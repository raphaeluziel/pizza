# Project 3 - Pizza

CS50 - Web Programming with Python and JavaScript

For this project we had to build a pizza ordering app to handle online orders.  The website has a page to see the entire menu with prices, a user authentication system, and and ordering and confirmation ability.  The app is built with Django, and on the admin part the pizza shop owner or administrator can add items, look at orders, etc... on that site.

I incorporated several personal touches to the app.  I used Sendgrid (sendgrid.com) to allow users who forgot their password to reset it by receiving an email with instructions.  Also, I used SendGrid so that users will receive and email confirmation when they submit an order.  The Stripe (stripe.com) to add the ability to receive payments via credit card.

The models I used are as follows.  Items stored information about the item (type, name, size, price, price for extras, etc...)  OrderItems model includes the Item, the quantity of that item, along with the order it is associated with).  The Order model has the customer, total price, timestamp included in it.  

I used postgres for the database as opposed to the default one.  The purpose of the files I created follows.  The checkout.js file is needed to handle the stripe credit card payments.  The menu.js file takes all the items from the database using an API AJAX call to the web server and builds the menu from that.  The order.js file is used to generate additional dropdwon menus for the toppings depending on how many toppings the pizza the user chose has.

The index.html is just a welcome or about page.  The menu.html shows the menu.  The order.htm is where users actually select items for their order - it also includes the shopping cart of all the items chosen.  Once the user hits submit, the user is taken to the checkout page, where credit card information is entered, and if successful to the confirmation page.  There is a your_orders page with all orders placed, along with their status, and for each order their is an order_details page listing the details of the order.

The working website is at https://pizza.raphaeluziel.net.
