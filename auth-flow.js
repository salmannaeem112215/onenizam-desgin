/* Prototype flows: no email is sent; any six digits advance the preview. */
(() => {
  const params = new URLSearchParams(location.search);
  const flow = params.get('flow') === 'signup' ? 'signup' : 'reset';
  const email = params.get('email') || '';
  const emailInput = document.getElementById('email');
  if (emailInput) emailInput.value = email;
  function verificationURL(email, flow) {
    return '/verify-code?' + new URLSearchParams({ email, flow });
  }
  function passwords(form, password, confirm) {
    password.required = confirm.required = true;
    password.minLength = 8;
    password.autocomplete = confirm.autocomplete = 'new-password';
    function validate() {
      const valid = password.value.length >= 8 && /[A-Z]/.test(password.value) && /[a-z]/.test(password.value) && /[0-9]/.test(password.value) && /[!@#$%^&*(),.?":{}|<>]/.test(password.value);
      password.setCustomValidity(valid ? '' : 'Use at least 8 characters with uppercase and lowercase letters, a number, and a symbol.');
      confirm.setCustomValidity(confirm.value === password.value ? '' : 'Passwords must match.');
    }
    password.addEventListener('input', validate);
    confirm.addEventListener('input', validate);
    form.addEventListener('submit', validate);
  }
  const forgot = document.getElementById('forgot-form');
  if (forgot) forgot.addEventListener('submit', event => {
    event.preventDefault();
    location.href = verificationURL(emailInput.value.trim(), 'reset');
  });
  const signup = document.getElementById('signup-form');
  if (signup) {
    passwords(signup, document.getElementById('signup-password'), document.getElementById('signup-confirm'));
    signup.addEventListener('submit', event => {
      event.preventDefault();
      if (signup.reportValidity()) location.href = verificationURL(emailInput.value.trim(), 'signup');
    });
  }
  const reset = document.getElementById('reset-form');
  if (reset) {
    passwords(reset, document.getElementById('new-password'), document.getElementById('confirm-password'));
    reset.addEventListener('submit', event => {
      event.preventDefault();
      if (reset.reportValidity()) location.href = '/password-updated';
    });
  }
  document.querySelectorAll('[data-toggle]').forEach(button => {
    button.addEventListener('click', () => {
      const input = document.getElementById(button.dataset.toggle);
      const show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      button.setAttribute('aria-pressed', String(show));
      button.setAttribute('aria-label', (show ? 'Hide ' : 'Show ') + input.placeholder.toLowerCase());
    });
  });
  const verify = document.getElementById('verify-form');
  if (verify) {
    if (!email) { location.replace('/forgot-password'); return; }
    document.getElementById('verification-email').textContent = email;
    document.getElementById('use-another-email').href = (flow === 'signup' ? '/create-account' : '/forgot-password') + '?' + new URLSearchParams({ email });
    const inputs = [...document.querySelectorAll('.auth-code')];
    const button = document.getElementById('verify-button');
    const update = () => { button.disabled = !inputs.every(input => /^\d$/.test(input.value)); };
    inputs.forEach((input, index) => {
      input.addEventListener('input', () => {
        input.value = input.value.replace(/\D/g, '').slice(-1);
        if (input.value && index < 5) inputs[index + 1].focus();
        update();
      });
      input.addEventListener('paste', event => {
        event.preventDefault();
        const digits = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
        if (!digits) return;
        const start = digits.length === 6 ? 0 : index;
        [...digits].forEach((digit, offset) => { if (inputs[start + offset]) inputs[start + offset].value = digit; });
        inputs[Math.min(start + digits.length, 5)].focus();
        update();
      });
      input.addEventListener('keydown', event => {
        if (event.key === 'Backspace' && !input.value && index > 0) inputs[index - 1].focus();
        if (event.key === 'ArrowLeft' && index > 0) inputs[index - 1].focus();
        if (event.key === 'ArrowRight' && index < 5) inputs[index + 1].focus();
      });
      input.addEventListener('focus', () => input.select());
    });
    verify.addEventListener('submit', event => {
      event.preventDefault();
      if (inputs.every(input => /^\d$/.test(input.value))) location.href = flow === 'signup' ? '/front-desk' : '/create-password';
    });
    inputs[0].focus();
  }
})();
