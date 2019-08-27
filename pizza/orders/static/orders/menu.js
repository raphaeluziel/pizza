document.addEventListener('DOMContentLoaded', () => {

  // Creates a table for each item type and populates it with items
  function drawTable(item_type, items, toppings, item_list)
  {
    i = 0;

    // Create a bookbark bar to jump to sections of the menu page
    const nav_bar = document.createElement('div');
    nav_bar.className = 'menu_nav';
    nav_bar.setAttribute('id', item_type.toLowerCase())

    item_list.forEach(function(item, index){
      link = document.createElement('a');
      span = document.createElement('span');
      link.setAttribute('href', '#' + item.toLowerCase());
      if (index < item_list.length - 1) {span.innerHTML = ' | '} else { span.innerHTML = ' '}
      link.innerHTML = item;
      nav_bar.appendChild(link);
      nav_bar.appendChild(span);
    });

    document.getElementById("menu").appendChild(nav_bar);

    // The toppings part of the menu is different than the other tables
    if (item_type === 'Toppings'){

      // Create a div to hold the toppings list
      const d = document.createElement('div');
      d.setAttribute('id', 'topps');
      d.setAttribute('style', 'text-align: center; width: 60%; margin: 20px 0px;');
      document.getElementById("menu").appendChild(d);

      // Create a div to title the toppings section
      const dh = document.createElement('div');
      dh.setAttribute('style', 'font-size: 110%; font-weight: bold; margin-bottom: 10px;');
      dh.innerHTML = 'Toppings';
      d.appendChild(dh)

      // Add each item in the topping list to the DOM
      toppings.forEach(function(x){
        var d2 = document.createElement('div');
        d2.innerHTML = x.topping;
        d.appendChild(d2);
      });

    }

    // Create a table for each of the other item types
    t = document.createElement('table');
    var row = t.insertRow(-1);
    var header = document.createElement('th');
    header.setAttribute('colspan', '3')
    header.innerHTML = item_type;
    row.appendChild(header);

    if((item_type !== 'Pasta') && (item_type !== 'Salad'))
      row = t.insertRow();
      var cell = row.insertCell(0);
      cell = row.insertCell(1);
      cell.innerHTML = 'Small';
      cell = row.insertCell(2);
      cell.innerHTML = 'Large';

    // Populate the table with the item names and prices
    while (i < items.length)
    {
      // Variables to hold row and cell nodes of the table
      var c, r;

      // Table should only hold items of that particular type
      if (items[i].type == item_type)
      {
        type = items[i].type;
        size = items[i].size;
        name = items[i].name || items[i].toppings;

        // Variables to hold prices for small or large sizes
        var small, large;

        if (size == 'Small') { small = items[i].price; large = items[i+1].price; i++; }
        else {small = ''; large = items[i].price}

        r = t.insertRow();
        c = r.insertCell(0);
        c.innerHTML = name;
        c = r.insertCell(1);
        c.innerHTML = small;
        c = r.insertCell(2);
        c.innerHTML = large;

        document.getElementById("menu").appendChild(t);
      };

      i++;
    }
  }

  // Get a list of objects from the database
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      var items = JSON.parse(this.responseText);

      // Create a list of item types
      var item_types = [];

      for (i = 0; i < items.length; i++)
      {
        if (item_types.indexOf(items[i].type) < 0){
          item_types.push(items[i].type);
        }
      }

      // Insert toppings into this list for inserting into the menu
      item_types.splice(2, 0, "Toppings");

      // Get a list of the toppings from the database
      var toppinghttp = new XMLHttpRequest();
      toppinghttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

          var toppings = JSON.parse(this.responseText);

          var first_item = 0;

          item_types.forEach(function(x){
            drawTable(x, items, toppings, item_types);
          });

        }
      };
      toppinghttp.open("GET", "toppingsAPI", true);
      toppinghttp.send();

    }
  };
  xmlhttp.open("GET", "menuAPI", true);
  xmlhttp.send();

});
