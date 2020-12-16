Vue.component('header-cart-items', {
    delimiters: ['[[', ']]'],
    props: ['item','index'],
    template: `
     <div class="header-cart__item">
                    <img :src="item.image" alt="">
                    <p><span class="color-green">[[index+1]].</span>[[item.name]]<br><span style="font-size: 12px;opacity: .5;">[[item.color]] | [[item.size]] | [[item.height]] x [[item.num]]шт</span>
                   </p>
                </div>
    `,
    methods: {
        userDelete: function(index){
            this.$emit('userdelete', index);
        }
    }
})


Vue.component('main-cart-item', {
    delimiters: ['[[', ']]'],
    props: ['item','index'],
    template :`  
    <div class="cart-item">
                    <div class="cart-item__img">
                        <img :src="item.image" alt="">
                    </div>
                    <div class="cart-item__info">
                        <p class="cart-item__info__art">арт. 234104</p>
                        <p class="cart-item__info__name">[[item.name]]<br>
                        <span style="font-size: 12px;opacity: .5;">[[item.color]] | [[item.size]] | [[item.height]]</span>
                        </p>

                     
                    </div>
                    <div class="cart-item__quantity">
                        <p @click="delQt(index)" class="cart-item__quantity--minus">-</p>
                        <p  class="cart-item__quantity--num">[[item.num]]</p>
                        <p @click="addQt(index)" class="cart-item__quantity--plus">+</p>
                    </div>
                    <div class="cart-item__price">[[item.price * item.num]] ₽</div>
                    <div @click="userDelete(index)" class="cart-item__delete">
                        <svg width="17" height="17" viewBox="0 0 17 17" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M1 16L16 1" stroke="#E0E0E0"/>
                            <path d="M16 16L0.999999 1" stroke="#E0E0E0"/>
                        </svg>

                    </div>
                </div>  
  `,

    methods: {
        userDelete: function (index) {
            this.$emit('userdelete', index);
        },
        delQt: function (index) {

            this.$emit('del_qt', index);
        },
        addQt: function (index) {
            this.$emit('add_qt', index);
        }
    }
})
Vue.component("modal", {
    template: "#modal-template"
});

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        tabActive:'profileTab',

        itemInfo:'444',
        selectedColor:999,
        selectedColorName:null,
        selectedSize:null,
        selectedSizeName:'Выберите цвет',
        selectedHeight:null,
        selectedHeightName:'Выберите цвет',
        sizes:null,
        deliveryPrice:0,
        heights:null,
        coords: [54.82896654088406, 39.831893822753904],
        cartTotal:0,
        cartTotalwPromo:0,
        cartItemsNum:0,
        cartNotEmpty : false,
        promo_percent:0,
        promo_rub:0,
        promo:null,
        sidePanelActive:false,
        mobileCatalogActive:false,
        headerCartShow:false,
        loginModal:false,
        menuOpen:false,
        registerModal:false,
        headerCartItems: [
        ],
        showModal: false

    },

    methods:{
        selectColor(index){
            console.log(index)
            this.selectedColor = this.itemInfo[index].color_id
            this.sizes = this.itemInfo[index].sizes
            this.heights = this.itemInfo[index].heights
            this.selectedColorName = this.itemInfo[index].color_name
            console.log(this.selectedColorName)
            this.selectedSizeName = 'Выберите размер'
            this.selectedHeightName = 'Выберите размер'
            console.log('this.sizes',this.sizes)


        },
        applyPromo(){
            if (!this.promo){
                this.errorToast('Введите промокод')
                return
            }
            let body={
                promo:this.promo
            }
            let csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
            fetch(`/user/apply_promo/`, {
                method: 'post',
                body: JSON.stringify(body),
                headers: { "X-CSRFToken": csrfmiddlewaretoken },
                credentials: 'same-origin'
            }).then(res=>res.json())
                .then(res => {
                    console.log(res)
                    if (res['status'] === true){
                        console.log(res)
                        Toastify({
                            duration: 1000,
                            close: true,
                            text: `Промокод применен`,
                            backgroundColor: "linear-gradient(to right, #aac1c1, #519999)",
                            className: "info",
                        }).showToast();
                        window.location.reload()
                    }else {
                        this.errorToast('Промокод не найден')
                    }


                })
        },
        selectSize(s_name,s_id,heights){
            console.log(heights)
            this.selectedHeightName = 'Выберите рост'
            this.selectedSize=s_id
            this.selectedSizeName=s_name
            this.heights = heights
            // console.log('this.heights',this.heights)
        },
        remove: function(index){
            let item_id =this.headerCartItems[index]['id'],
                btn = document.getElementById(`add_btn_${item_id}`)
            try {
                btn.removeAttribute('disabled')
                btn.innerText = 'В корзину'
            }
            catch (e) {

            }


            this.headerCartItems.splice(index, 1)
            this.sendUpdateRequest(item_id,'del_item')
            Toastify({
                duration: 1000,
                close: true,
                text: `Товар удален из корзины`,
                backgroundColor: "linear-gradient(to right, #f55f63, #be353b)",
                className: "info",
            }).showToast();


        }
        ,
        del_qt: function (index) {
            if (this.headerCartItems[index]['num'] > 1){
                this.headerCartItems[index]['num'] -= 1
                this.updateCart(this.headerCartItems[index]['id'],this.headerCartItems[index]['num'])
            }
        },
        add_qt: function (index) {
            this.headerCartItems[index]['num'] += 1
            this.updateCart(this.headerCartItems[index]['id'],this.headerCartItems[index]['num'])
        },
        updateCart: function (item_id,num) {
            console.log('update',item_id,num)
            this.cartTotal = 0
            for(var item in this.headerCartItems){
                console.log(this.headerCartItems[item]['price'])
                this.cartTotal +=  parseInt(this.headerCartItems[item]['price']) * parseInt(this.headerCartItems[item]['num'])
            }
            this.sendUpdateRequest(item_id,'set_num',num)
        },
        sendUpdateRequest: function(item_id,action,num='1'){
            let csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value,
                overlay = document.getElementById('cart_overlay'),
                body = {item_id:item_id,
                    action:action,
                    number:num}
            if (overlay){overlay.classList.add('cart-overlay-active')}

            fetch(`/cart/add_to_cart/`, {
                method: 'post',
                body: JSON.stringify(body),
                headers: { "X-CSRFToken": csrfmiddlewaretoken },
                credentials: 'same-origin'
            }).then(res=>res.json())
                .then(res => {
                    if (res['result'] === true){
                        console.log(res)

                    }
                    if (overlay){overlay.classList.remove('cart-overlay-active')}

                })
        },
        errorToast(text){
            Toastify({
                duration: 1000,
                close: true,
                text: `${text} `,
                backgroundColor: "linear-gradient(to right, #f55f63, #be353b)",
                className: "info",
            }).showToast();
        },
        addItem: function (name,image,id) {
            if (this.selectedColor===999){
                this.errorToast('Выберите цвет')
                return
            }
            if (!this.selectedSize){
                this.errorToast('Выберите размер')
                return
            }
            if (!this.selectedHeight){
                this.errorToast('Выберите рост')
                return
            }
            console.log('add')
            // this.headerCartItems.push({
            //     name:name,
            //     image:image,
            //     color:this.selectedColorName,
            //     size:this.selectedSizeName,
            //     height:this.selectedHeightName
            // })
            let csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
            let data = {
                item_id: id,
                color:this.selectedColor,
                size:this.selectedSize,
                height:this.selectedHeight,
                action:'add_new'
            }
            fetch(`/cart/add_to_cart/`, {

                method: 'post',
                body: JSON.stringify(data),
                headers: { "X-CSRFToken": csrfmiddlewaretoken },
                credentials: 'same-origin'
            }).then(res=>res.json())
                .then(res => {
                    if (res['result'] === true){
                        console.log(res)
                        getCart()
                    }


                })
            Toastify({
                duration: 1000,
                close: true,
                text: `${name} добавлен в корзину`,
                backgroundColor: "linear-gradient(to right, #aac1c1, #519999)",
                className: "info",
            }).showToast();
        },
        addInFav:function (event) {
            console.log('addinfav',event.target.classList.contains('fa-heart-o'))

            let csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value,
                body = {item_id:event.target.getAttribute('data-id')},
                text=''


            console.log(body)
            fetch(`/cart/add_to_fav/`, {
                method: 'post',
                body: JSON.stringify(body),
                headers: { "X-CSRFToken": csrfmiddlewaretoken },
                credentials: 'same-origin'
            }).then(res=>res.json())
                .then(res => {

                    console.log(res)
                    event.target.classList.toggle('item-in-fav')
                    if (res['result']==='deleted'){text='Товар удален из избранного'}
                    if (res['result']==='added'){text='Товар добавлен в избранное'}

                    Toastify({
                        duration: 1000,
                        close: true,
                        text: text,
                        backgroundColor: "linear-gradient(to right, #f55f63, #be353b)",
                        className: "info",
                    }).showToast();
                })
        },
    },
    watch: {
        headerCartItems: function (val) {
            console.log('change')
            console.log('promo_percent',this.promo_percent)
            console.log('promo_rub',this.promo_rub)
            this.cartTotal = 0
            let x = 0

            for(var item in val){
                console.log(val[item]['price'])
                this.cartTotal +=  parseInt(val[item]['price']) * parseInt(val[item]['num'])
                x+=1
            }

            if (parseInt(this.promo_percent)>0){
                this.cartTotalwPromo = this.cartTotal - (this.cartTotal * parseInt(this.promo_percent) / 100)
            }
            if (parseInt(this.promo_rub)>0){
                this.cartTotalwPromo = this.cartTotal - parseInt(this.promo_rub)
            }

            this.cartItemsNum = x

        }
    }
})
