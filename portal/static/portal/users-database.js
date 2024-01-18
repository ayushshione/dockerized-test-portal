
function showModal(){
  const modal = document.getElementById('modal-sam')

  modal.classList.remove('hidden');
  modal.classList.add('flex')
}

document.getElementById('hide-modal').addEventListener('click', (e) => {
  e.preventDefault();
  const modal = document.getElementById('modal-sam')

  modal.classList.remove('flex');
  modal.classList.add('hidden')
})

