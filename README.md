# 🐉 The Dragon’s Hoard Barmoury

**Live Demo:** [The Dragon’s Hoard Barmoury on Heroku](https://squat-llama-c5e1f1c2daa0.herokuapp.com/)

_The Dragon’s Hoard Barmoury_ is a simulated fantasy-themed digital storefront built with Django. It demonstrates a complete e-commerce experience with user authentication, product listings, reviews, and a rudimentary cart system. This project was created as a full-stack capstone to showcase minimum viable product functionality for an e-commerce site while integrating responsive design and accessible UX principles.

---

## 📋 Project Overview
The project explores the idea of “what if a fantasy shopkeeper had a website?” Users can browse products, submit reviews, and interact with a simple cart system. The project uses Django's default User model, model forms, and custom apps for products, reviews, and cart items. The cart persists across sessions and allows users to clear items or view a total calculation. Although there are quantity buttons and an "Order Now" feature, these are currently rudimentary placeholders, with "Order Now" clearing the cart and returning the user to the home page.

The goal was to create a focused and functional MVP of an e-commerce site with a coherent fantasy identity, while providing a responsive and modern interface for users.

---

## ⚙️ Features and Technical Stack
**Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript  
**Backend:** Python 3, Django 5  
**Database:** PostgreSQL (Heroku Postgres)  
**Static & Media Storage:** Cloudinary for product images  
**Authentication:** Django auth + django-allauth  
**Forms & UX:** Django ModelForms, crispy-bootstrap5  
**AI Tools:** GitHub Copilot for scaffolding code and ChatGPT for clarifying logic and documentation  
**Deployment:** Heroku (Gunicorn + Whitenoise) 

**Key Features:**
- Product listings with images and categories (category filtering to be added in future).  
- User-submitted product reviews with rating scores.  
- Persistent cart system powered by `Cart_Item` model.  
- Admin dashboard to manage products and reviews.  
- Fully responsive navigation and layout with consistent styling.  
- Session persistence and secure CRUD operations for users and data.  
- Accessibility considerations throughout forms and templates.

---

## 💻 Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/the-dragons-hoard-barmoury.git
cd the-dragons-hoard-barmoury

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Run the server locally
python manage.py runserver
```

---

## 🗄️ Data Models & Business Logic
**Product Model:** Contains `name`, `description`, `price`, `image`, and `category`. Images are stored on Cloudinary, sourced from 3D artists on Sketchfab.  

**Review Model:** Links users to products with `rating`, `comment`, and `created_at`. Users may only submit one review per product.  

**Cart_Item Model:** Associates products with users and tracks quantity. The `subtotal()` method calculates the line total for display.  

Example:
```python
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Cart_Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stagedproduct")
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name}'
```

**Cart Behavior:**  
- Persists across sessions for logged-in users.  
- Users can clear their cart, view totals, and adjust quantities in the future.  
- The "Order Now" button currently clears the cart without processing payment.  

---

## 🔐 Authentication & Authorization
- Only users and admins exist.  
- Login, registration, and logout use Django auth and allauth.  
- Admin users have access to Django’s admin dashboard.  
- Admin dashboard does include a custom action to list/de-list items.
- Routes requiring authentication include review submission and cart viewing.  

---

## 🧪 Testing
- Django `TestCase` used to test models, views, and forms.  
- HTML Validation using W3's HTML Validation Tool
![Screenshot of W3's HTML Validator, showing only minor warnings.](https://github.com/SourTarte/fantasy-storefront/tree/main/readme-imgs/html-validation.png)
- Browser testing via Chrome DevTools. 
![Screenshot of the deployed site with Chrome's Lighthouse tool open.](https://github.com/SourTarte/fantasy-storefront/tree/main/readme-imgs/lighthouse-test.png)
	- Best Practices' low score was mostly attributed to Cloudinary's lack of HTTPS usage.
- Peer testing helped identify issues such as adding items to the cart while logged out (which previously caused 500 errors).  
- Copilot generated initial test scaffolds, later manually corrected.  
- Tests cover: product creation, review submission, cart operations, and user authentication.  

---

## ☁️ Deployment
- Deployed on Heroku using PostgreSQL and Gunicorn.  
- Static and media files served with Whitenoise.  
- Environment variables managed via `.env` (kept out of Git).  
- Deployment challenges included missing Procfile and environment variable setup.  
- Minimal branching workflow; branches were named after features/bugs.  

---

## 🤖 AI-Augmented Development
- Copilot assisted with the initial scaffolding of the cart system and some bug fixes.  
- ChatGPT helped clarify logic and produce more understandable documentation and metaphors.  
- Copilot sometimes offered incorrect test cases, which were manually corrected.  
- AI improved speed and understanding but hands-on problem-solving remained central to learning.  

---

## 🚀 Agile Planning & UX Design
- Planning and documentation tracked in Obsidian with Kanban plugin.
![Screenshot of Obsidian Markdown Editor, showing a Kanban board within it.](https://github.com/SourTarte/fantasy-storefront/tree/main/readme-imgs/kanban-board.png)

- Wireframes created in Adobe Illustrator with inspiration from LARPing and medieval replica websites.  
![Wireframe of a web layout as shown on a mobile layout.](https://github.com/SourTarte/fantasy-storefront/tree/main/readme-imgs/wireframe-mobile.webp)

- Responsive and modern UI design with Bootstrap 5, Flexbox, and semantic HTML.  
- Accessibility checks for colour contrast, labels, and navigation.  
- Iterative user testing informed interface improvements.  

---

## 💬 Reflections

**Challenges:**  
- Collating item IDs and quantities for the cart system.  
- Database conflicts and debugging logic for reviews and cart persistence.  

**Proud Achievements:**  
- Seamless cart implementation and responsive navbar on both desktop and mobile.  
- Modern interface design with fantasy theming.  

**Future Enhancements:**  
- Implement saved wishlists.  
- Enable quantity editing in the cart.  
- Redesign cart as a live-update Bootstrap modal.  

---

## 🎨 3D Model & Image Credits
Any usage of this project must include the following attributions, as they are licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/):

- Image of "[Fantasy_sword_25_with_scabbard](https://skfb.ly/oMqTn)" by Nicu_Tepes_Vulpe  
- Image of "[Fantasy_sword_11](https://skfb.ly/oLsUV)" by Nicu_Tepes_Vulpe  
- Image of "[Fantasy 2 handed Sword](https://skfb.ly/L8oW)" by xrenou  
- Image of "[Fantasy Axe (optimised for games)](https://skfb.ly/oxMxD)" by Ashraf Bouhadida  
- Image of "[Drakefire Pistol](https://skfb.ly/6xCGp)" by Teliri  
- Image of "[Fantasy Longsword](https://skfb.ly/ontRY)" by Faber  
- Image of "[Fantasy Axe](https://skfb.ly/oQQ7R)" by Mikołaj Michalak  
- Image of "[Bow and Arrow](https://skfb.ly/6YKo6)" by Amatsukast  
- Image of "[Medieval crosbow](https://skfb.ly/6SxQx)" by Cyril43  
- Image of "[Free Female Fantasy Armor - 2](https://skfb.ly/oSKvz)" by Kaan Tezcan  
- Image of "[FREE Magical Assassin](https://skfb.ly/proYZ)" by Axinovium  

---

### 🧾 License

This project was created for educational purposes as part of the **AI-Augmented Full Stack Bootcamp (Django Framework)**.
