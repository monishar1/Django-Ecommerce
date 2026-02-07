const products_container = document.querySelector("#products-container");
let cart_count = document.querySelector("#cart-count");

// =============================
// LOAD CART COUNT
// =============================
async function loadcartCount() {
    if (!cart_count) return;

    const countUrl = cart_count.dataset.countUrl;
    try {
        const result = await fetch(countUrl);
        const data = await result.json();
        cart_count.innerHTML = data.cart_count;   // FIXED (=)
    }
    catch (error){
        console.error(`Cart count fetch error : ${error}`)
    }
}
if (cart_count){
    loadcartCount();   // FIXED (call the function)
}

// =============================
// CSRF TOKEN (renamed to avoid conflict)
// =============================
function getToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// =============================
// ADD TO CART (only if container exists)
// =============================
if (products_container) {
    const addUrl = products_container.dataset.addUrl;

    products_container.addEventListener('click', async function (event) {
        if(!event.target.classList.contains('add-to-cart')) return;

        const btn = event.target;
        const product_card = btn.closest(".product-card");
        const productId = product_card.dataset.productId;

        btn.disabled = true;

        try{
            const response = await fetch(addUrl, {
                method : 'POST',
                headers : {
                    'X-CSRFToken': getToken(),
                    "Content-Type" : "application/x-www-form-urlencoded" // FIXED case
                },
                body : `product_id=${productId}`
            })
            const data = await response.json();

            if (response.status === 401 && data.redirect_url){
                window.location.href = data.redirect_url;
                return;
            }
            if (data.cart_count !== undefined && cart_count){
                cart_count.innerHTML = data.cart_count;
            }
        }
        catch(error){
            console.error(`cart error ${error}`)    
        }
        finally{
            btn.disabled = false;
            btn.innerText = "Add to Cart"
        }
    });
}

// =============================
// INCREASE
// =============================
document.querySelectorAll(".increase").forEach(btn => {
    btn.onclick = function () {
        let id = this.dataset.id;

        fetch("/cart/increase/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "product_id=" + id
        })
        .then(res => res.json())
        .then(data => {
            const el = document.getElementById("qty-" + id);
            if (el) el.innerText = data.qty;
        });
    }
});

// =============================
// DECREASE
// =============================
document.querySelectorAll(".decrease").forEach(btn => {
    btn.onclick = function () {
        let id = this.dataset.id;

        fetch("/cart/decrease/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "product_id=" + id
        })
        .then(res => res.json())
        .then(data => {
            if (data.qty == 0) {
                location.reload();
            } else {
                const el = document.getElementById("qty-" + id);
                if (el) el.innerText = data.qty;
            }
        });
    }
});

// =============================
// REMOVE
// =============================
document.querySelectorAll(".remove").forEach(btn => {
    btn.onclick = function () {
        let id = this.dataset.id;

        fetch("/cart/remove/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "product_id=" + id
        })
        .then(res => res.json())
        .then(() => {
            location.reload();
        });
    }
});
