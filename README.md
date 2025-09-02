<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

</head>
<body>

<h1>API Operation Project</h1>
<p><strong>Courier & Flip_Cart E-commerce API</strong> - Full-featured Django REST API with JWT authentication, product, cart, order, and delivery management.</p>

<h2>🌟 Key Features</h2>
<ul>
  <li>User authentication with email & JWT tokens</li>
  <li>Category & Product management with Cloudinary images</li>
  <li>Cart & Order processing, payment tracking</li>
  <li>Delivery assignment & order status updates</li>
  <li>Interactive Swagger & Postman API documentation</li>
  <li>Professional Admin Panel for monitoring</li>
</ul>

<h2>🛠 Tech Stack</h2>
<ul>
  <li>Backend: Python, Django, Django REST Framework</li>
  <li>Authentication: JWT (Bearer tokens)</li>
  <li>Database: SQLite (can upgrade to PostgreSQL)</li>
  <li>Media Storage: Cloudinary</li>
  <li>API Docs: Swagger UI & Postman Collection</li>
</ul>

<h2>🚀 Quick Start</h2>
<pre><code>git clone https://github.com/sojibhasan5800/api_operation.git
cd api_operation
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
</code></pre>
<p>Admin Panel: <a href="http://127.0.0.1:8000/admin/" target="_blank">http://127.0.0.1:8000/admin/</a></p>

<h2>📑 API Documentation</h2>
<ul>
  <li>Swagger UI: <a href="http://127.0.0.1:8000/swagger/" target="_blank">http://127.0.0.1:8000/swagger/</a></li>
  <li>Postman Collection: <a href="#" target="_blank">Download Here</a></li>
</ul>

<h2>🔑 Authentication</h2>
<p>JWT Bearer tokens for all protected endpoints. Email login supported via custom backend.</p>
<pre><code>Authorization: Bearer &lt;your_access_token&gt;</code></pre>

<h2>📌 Key Endpoints</h2>
<table>
<tr><th>Module</th><th>Endpoint</th><th>Method</th><th>Description</th></tr>
<tr><td>Account</td><td>/api/v1/account/register/</td><td>POST</td><td>User registration</td></tr>
<tr><td>Account</td><td>/api/v1/account/login/</td><td>POST</td><td>Email login</td></tr>
<tr><td>Categories</td><td>/api/v1/categories/</td><td>GET/POST</td><td>List & create categories</td></tr>
<tr><td>Store</td><td>/api/v1/store/</td><td>GET/POST</td><td>List & add products</td></tr>
<tr><td>Cart</td><td>/api/v1/cart/</td><td>GET/POST</td><td>Manage user cart</td></tr>
<tr><td>Orders</td><td>/api/v1/order/orders/create_api/</td><td>POST</td><td>Create user order</td></tr>
<tr><td>Orders</td><td>/api/v1/order/orders/delivery_api/</td><td>GET</td><td>List delivery orders</td></tr>
<tr><td>Orders</td><td>/api/v1/order/&lt;id&gt;/update-status/</td><td>PATCH</td><td>Update order status</td></tr>
</table>

<h2>💡 HR / QA Highlights</h2>
<ul>
  <li>Swagger UI & Postman for instant API testing</li>
  <li>Modern email login + JWT token security</li>
  <li>Professional Admin panel ready for monitoring</li>
  <li>Short, modular, and scalable project structure</li>
</ul>


</body>
</html>
