(() => {
  const form = document.getElementById('discoveryForm');
  if (!form) return;

  const steps = [...document.querySelectorAll('.form-step')];
  const questionBlocks = [...document.querySelectorAll('[data-question]')];
  const progressBar = document.getElementById('progressBar');
  const stepCounter = document.getElementById('stepCounter');
  const stepTitle = document.getElementById('stepTitle');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const submitBtn = document.getElementById('submitBtn');
  const reviewContent = document.getElementById('reviewContent');
  const saveState = document.getElementById('saveState');
  const formErrors = document.getElementById('formErrors');
  const successPanel = document.getElementById('successPanel');
  const formCard = form.closest('.form-card');

  const storageKey = 'prdsystem:voyage:client-brief:v2';
  let currentStep = 0;
  let saveTimer;

  function questionValue(block) {
    const id = block.dataset.id;
    const type = block.dataset.type;
    if (type === 'checkboxes') {
      return [...block.querySelectorAll(`input[name="${CSS.escape(id)}"]:checked`)].map(el => el.value);
    }
    if (type === 'radio') {
      const selected = block.querySelector(`input[name="${CSS.escape(id)}"]:checked`);
      return selected ? selected.value : '';
    }
    if (type === 'checkbox') {
      const input = block.querySelector(`input[name="${CSS.escape(id)}"]`);
      return Boolean(input && input.checked);
    }
    const input = block.querySelector(`[name="${CSS.escape(id)}"]`);
    return input ? input.value.trim() : '';
  }

  function collectAnswers() {
    const answers = {};
    questionBlocks.forEach(block => {
      answers[block.dataset.id] = questionValue(block);
    });
    return answers;
  }

  function isEmpty(value) {
    if (Array.isArray(value)) return value.length === 0;
    if (typeof value === 'boolean') return value === false;
    return !String(value || '').trim();
  }

  function setQuestionValue(block, value) {
    const id = block.dataset.id;
    const type = block.dataset.type;
    if (type === 'checkboxes') {
      const values = Array.isArray(value) ? value : [];
      block.querySelectorAll(`input[name="${CSS.escape(id)}"]`).forEach(input => {
        input.checked = values.includes(input.value);
      });
      return;
    }
    if (type === 'radio') {
      block.querySelectorAll(`input[name="${CSS.escape(id)}"]`).forEach(input => {
        input.checked = input.value === value;
      });
      return;
    }
    if (type === 'checkbox') {
      const input = block.querySelector(`input[name="${CSS.escape(id)}"]`);
      if (input) input.checked = value === true;
      return;
    }
    const input = block.querySelector(`[name="${CSS.escape(id)}"]`);
    if (input && typeof value === 'string') input.value = value;
  }

  function saveDraft() {
    const draft = {
      step: Math.min(currentStep, steps.length - 2),
      answers: collectAnswers(),
      savedAt: new Date().toISOString(),
    };
    try {
      localStorage.setItem(storageKey, JSON.stringify(draft));
      saveState.textContent = 'تم حفظ تقدمك';
      clearTimeout(saveTimer);
      saveTimer = setTimeout(() => {
        saveState.textContent = 'يتم حفظ تقدمك تلقائياً';
      }, 1400);
    } catch (_) {
      saveState.textContent = 'تعذر الحفظ المحلي';
    }
  }

  function restoreDraft() {
    try {
      const raw = localStorage.getItem(storageKey);
      if (!raw) return;
      const draft = JSON.parse(raw);
      if (draft && draft.answers) {
        questionBlocks.forEach(block => {
          if (Object.prototype.hasOwnProperty.call(draft.answers, block.dataset.id)) {
            setQuestionValue(block, draft.answers[block.dataset.id]);
          }
        });
      }
      if (Number.isInteger(draft.step)) currentStep = Math.max(0, Math.min(draft.step, steps.length - 2));
    } catch (_) {
      localStorage.removeItem(storageKey);
    }
  }

  function clearError(block) {
    block.classList.remove('has-error');
    const error = block.querySelector('.field-error');
    if (error) error.textContent = '';
  }

  function setError(block, message) {
    block.classList.add('has-error');
    const error = block.querySelector('.field-error');
    if (error) error.textContent = message;
  }

  function validateStep(index) {
    if (index >= steps.length - 1) return true;
    let valid = true;
    const blocks = [...steps[index].querySelectorAll('[data-question]')];
    blocks.forEach(block => {
      clearError(block);
      if (block.dataset.required !== '1') return;
      const value = questionValue(block);
      if (isEmpty(value)) {
        setError(block, 'هذا السؤال مهم عشان نقدر نفهم المشروع قبل الانتقال.');
        valid = false;
      }
    });
    if (!valid) {
      const first = steps[index].querySelector('.has-error');
      if (first) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    return valid;
  }

  function displayValue(raw) {
    if (Array.isArray(raw)) return raw.join('، ');
    if (typeof raw === 'boolean') return raw ? 'نعم' : 'لا';
    return String(raw || '');
  }

  function renderReview() {
    const answers = collectAnswers();
    reviewContent.innerHTML = '';

    const answeredCount = Object.values(answers).filter(value => !isEmpty(value)).length;
    const summary = document.createElement('div');
    summary.className = 'review-summary';
    summary.innerHTML = `<strong>ممتاز، وصلنا أساس الفكرة.</strong><span>جاوبت على ${answeredCount} نقاط. تحت ملخص لأهم المعلومات فقط.</span>`;
    reviewContent.appendChild(summary);

    const coreIds = ['project_vision', 'core_problem', 'current_process', 'must_haves'];
    coreIds.forEach(id => {
      const block = questionBlocks.find(item => item.dataset.id === id);
      if (!block) return;
      const raw = answers[id];
      if (isEmpty(raw)) return;

      const item = document.createElement('div');
      item.className = 'review-item review-item-compact';
      const label = document.createElement('strong');
      label.textContent = block.dataset.label;
      const value = document.createElement('p');
      value.textContent = displayValue(raw);
      item.append(label, value);
      reviewContent.appendChild(item);
    });
  }

  function showStep(index) {
    currentStep = Math.max(0, Math.min(index, steps.length - 1));
    steps.forEach((step, i) => { step.hidden = i !== currentStep; });

    const isReview = currentStep === steps.length - 1;
    const percentage = ((currentStep + 1) / steps.length) * 100;
    progressBar.style.width = `${percentage}%`;
    stepCounter.textContent = isReview ? 'الخطوة الأخيرة' : `الخطوة ${currentStep + 1} من ${steps.length - 1}`;
    stepTitle.textContent = steps[currentStep].dataset.title || 'Client Brief';
    prevBtn.hidden = currentStep === 0;
    nextBtn.hidden = isReview;
    submitBtn.hidden = !isReview;

    if (isReview) renderReview();
    saveDraft();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  nextBtn.addEventListener('click', () => {
    if (!validateStep(currentStep)) return;
    showStep(currentStep + 1);
  });

  prevBtn.addEventListener('click', () => showStep(currentStep - 1));

  form.addEventListener('input', (event) => {
    const block = event.target.closest('[data-question]');
    if (block) clearError(block);
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveDraft, 350);
  });

  form.addEventListener('change', saveDraft);

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    formErrors.hidden = true;
    formErrors.textContent = '';

    const answers = collectAnswers();
    const payload = {
      answers,
      website: document.getElementById('website').value,
      meta: {
        formVersion: 'voyage-client-brief-v2',
        language: 'ar',
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || '',
      },
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'جاري الإرسال...';

    try {
      const response = await fetch('/api/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const result = await response.json();
      if (!response.ok || !result.ok) {
        const errors = result.errors || ['تعذر إرسال النموذج. حاول مرة ثانية.'];
        formErrors.textContent = errors.join(' • ');
        formErrors.hidden = false;
        return;
      }

      localStorage.removeItem(storageKey);
      form.hidden = true;
      formCard.querySelector('.form-head').hidden = true;
      formCard.querySelector('.progress-track').hidden = true;
      document.getElementById('referenceId').textContent = result.reference;
      successPanel.hidden = false;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (_) {
      formErrors.textContent = 'تعذر الاتصال بالسيرفر. حاول مرة ثانية.';
      formErrors.hidden = false;
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'إرسال التصور';
    }
  });

  restoreDraft();
  showStep(currentStep);
})();
