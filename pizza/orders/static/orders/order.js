document.addEventListener('DOMContentLoaded', () => {

  document.getElementById('SubExtras').style.display = 'block';




});

function addToppings(x){
  var sel = document.getElementById(x);
  var opt = sel.options[sel.selectedIndex];
  var numExtras = opt.dataset.numextras;

  for (var i = 0; i < 5; i++){
    document.getElementById(x + i).style.display = 'none';
  }

  for (var i = 0; i < numExtras; i++){
    document.getElementById(x + i).style.display = 'flex';
  }
}
