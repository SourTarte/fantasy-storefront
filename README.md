# 🐉 The Dragon’s Hoard Barmoury

**Live Demo:** [The Dragon’s Hoard Barmoury on Heroku](https://squat-llama-c5e1f1c2daa0.herokuapp.com/)

_The Dragon’s Hoard Barmoury_ is a simulated fantasy-themed digital storefront built with Django. It demonstrates a complete e-commerce experience with user authentication, product listings, reviews, and a rudimentary cart system. This project was created as a full-stack capstone to showcase minimum viable product functionality for an e-commerce site while integrating responsive design and accessible UX principles.

## Contents
- [📋 Project Overview](#-project-overview)
- [⚙️ Features and Technical Stack](#️-features-and-technical-stack)
- [💻 Installation](#-installation)
- [🗄️ Data Models & Business Logic](#️-data-models--business-logic)
- [🔐 Authentication & Authorization](#-authentication--authorization)
- [🧪 Testing](#-testing)
- [☁️ Deployment](#️-deployment)
- [🤖 AI-Augmented Development](#-ai-augmented-development)
- [🚀 Agile Planning & UX Design](#-agile-planning--ux-design)
- [💬 Reflections](#-reflections)
- [🎨 3D Model & Image Credits](#-3d-model--image-credits)
- [🧾 License](#-license)
- [🐍 Code Style](#-code-style)


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
- User-attached wishlisting, with the ability to turn a cart into a wishlist.
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

**Wishlist_Item Model:** Associated a product with a Wishlist, creating a user-curated record of desired products.

**Wishlist Model:** Acts as a layer of seperation between Wishlist_Item and User, leaving scope open to expand functionality with multiple wish lists.

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
- HTML Validation using W3's HTML Validation Tool
![Screenshot of W3's HTML Validator, showing only minor warnings.](/readme-imgs/html-validation.png)
- Browser testing via Chrome DevTools. 
![Screenshot of the deployed site with Chrome's Lighthouse tool open.](/readme-imgs/lighthouse-test.png)
#### Usability testing

Throughout the project, accessibility testing was paramount. Colour contrast testing was performed early on, and usability testing was consistent through the project, to highlight any common UX pitfalls. Peer testing helped identify issues such as adding items to the cart while logged out (which previously caused 500 errors).  
#### Unit testing

This project includes a suite of unit tests under `shop/` to validate admin actions, cart behaviour, and forms. Tests are runnable with Django's built-in test runner using the command `python manage.py test`.

Common issues and fixes
- Missing model fields or migrations: tests assume `Product`, `Cart_Item`, `Wishlist_Item`, and related fields exist. Issue is resolved by running:
  ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```
- Template/button CSRF issues: While running tests, I ran into the issue of making sure that only one `{% csrf_token %}` was present per submitting form, and that `formaction` POSTs included the outer token.

AI involvement
- Initial test scaffolding, example assertions, and helper JS snippets were generated with assistance from GitHub Copilot. The generated code was reviewed and adapted to match the project structure.
- Use the tests as a starting point, adjusting fields to match my final models and views.

What was learned from writing/running the tests
- Tests quickly revealed missing or incomplete model definitions (implement `Product` and `Cart_Item` fields required by tests).
- Template forms and CSRF placement matter for `formaction` buttons — extra tokens inside buttons can break POSTs.
- Sorting and line-total logic are simplest and most reliable when implemented server-side. If done client-side, data attributes need to be included for price/quantity, and also update totals should be included on DOM load or after AJAX changes.
- Returning JSON from server endpoints simplifies non-blocking UI feedback (alerts/toasts) for wishlist and cart updates.


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
During the project, a codified list of 5 core goals were formed. These pillars were:
1. Deliver a functional fantasy-themed e-commerce MVP
2. Implement a complete user review workflow
3. Establish clear, accessible product information
4. Build a navigation structure that reduces friction
5. Ensure responsive behaviour across device sizes

- During the project, planning and documentation were tracked in Obsidian with a Kanban plugin.
![Screenshot of Obsidian Markdown Editor, showing a Kanban board within it.](/readme-imgs/kanban-board.png)
- For ease of use and accessibility, this board was later ported over to Github Projects , viewable [here](https://github.com/users/SourTarte/projects/8).
![Screenshot of the Github Project page for this project.](/readme-imgs/kanban-board-github.png)
- Wireframes created in Adobe Illustrator with inspiration from LARPing and medieval replica websites.  
![Wireframe of a web layout as shown on a mobile layout.](/readme-imgs/wireframe-mobile.webp)
---
## 💬 Reflections

**Challenges:**  
- Collating item IDs and quantities for the cart system.  
- Database conflicts and debugging logic for reviews and cart persistence.
- Some beginning friction with relation to Django's app-based logic.

**Proud Achievements:**  
- Responsive cart and navbar implementation for both desktop and mobile.
- Seamless wishlisting and product list sorting.
- Modern interface design, blending readability with a fantasy theming.  

**Future Enhancements:**  
- ~~Implement saved wishlists.~~
- ~~Enable quantity editing in the cart.~~
- Implement the ability to save multiple wishlists.
- Add aggregate reviews, displaying averages on product cards.
- Redesign cart using AJAX to implement product updates without page reloads.

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

## 🐍 Code Style

All Python code in this project adheres to [PEP 8 – Style Guide for Python Code](https://pep8.org/). Code style is enforced using [flake8](https://flake8.pycqa.org/).
