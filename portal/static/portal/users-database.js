
function showModal(){
  const modal = document.getElementById('modal-sam')
  const add_user = document.getElementById('add-user')
  const modal_button = document.getElementById('modal-button')

  add_user.disabled = true;
  modal_button.disabled = true;

  modal.classList.remove('hidden');
  modal.classList.add('flex')
}

function changeLoc(){
  window.location.href = '/add-user'
}

document.getElementById('hide-modal').addEventListener('click', (e) => {
  e.preventDefault();
  const modal = document.getElementById('modal-sam')
  const add_user = document.getElementById('add-user')
  const modal_button = document.getElementById('modal-button')

  add_user.disabled = false;
  modal_button.disabled = false;

  modal.classList.remove('flex');
  modal.classList.add('hidden')
})

