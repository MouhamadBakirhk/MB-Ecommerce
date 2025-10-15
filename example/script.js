let products = [
    {id:1, name:'t-shirt', price: 10, description:"cotton t-shirt"},
    {id:2, name:"Book", price:15, description:"Interesting novel"}
];

const container = document.getElementById("products");

products.forEach(p => {
  container.innerHTML += `
    <div>${p.name} - $${p.price}
      <button onclick="addToCart(${p.id})">Add to Cart</button>
    </div>`;
});

let cart = [];

function addToCart(id){
  let product = products.find(p => p.id === id);
  cart.push(product);
  alert(product.name + " added!");
}

function sendMessage(){
  let input = document.getElementById("chatbot-input");
  let message = input.value;
  let messages = document.getElementById("chatbot-messages");
  
  messages.innerHTML += `<div>User: ${message}</div>`;
  messages.innerHTML += `<div>Bot: sorry, I didn't understand.</div>`;
  
  input.value="";
}
