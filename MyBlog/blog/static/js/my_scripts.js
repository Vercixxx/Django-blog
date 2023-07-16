const toastTrigger = document.getElementById('liveToastBtn');
const toastLiveExample = document.getElementById('liveToast');
const form = document.getElementById('myForm');

if (toastTrigger) {
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
  toastTrigger.addEventListener('click', (event) => {
    event.preventDefault(); // Zatrzymaj domyślne zachowanie przeglądarki
    toastBootstrap.show();
    form.submit(); // Wyślij formularz ręcznie
  });
}
