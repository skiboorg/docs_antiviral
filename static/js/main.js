Vue.component('header-cart-items', {
    delimiters: ['[[', ']]'],
    props: ['item','index'],
    template: `<div class="header-cart-item">
                    <img :src="[[item.image]]" alt="">
                    <div class="header-cart-item-info">
                        <p>[[item.name]]</p>
                        <span class="header-cart-item-info-num">[[item.num]]</span>
                        x
                        <span class="header-cart-item-info-price">[[item.price]] <i class="fa fa-rub"></i> </span>
                        =
                        <span class="header-cart-item-info-total">[[item.num * item.price]] <i class="fa fa-rub"></i></span>
                    </div>                                           
                    <div class="header-cart-item-remove">
                        <i v-on:click="userDelete(index)" class="fa fa-times"></i>
                    </div>       
                </div>`,
    methods: {
        userDelete: function(index){
            this.$emit('userdelete', index);
        }
    }
})


Vue.component('main-cart-item', {
    delimiters: ['[[', ']]'],
    props: ['item','index'],
    template :`  <div class="main-cart-item">
 
                    <div class="main-cart-item-name">
                    
                        <img :src="[[item.image]]" alt=""> <span>[[item.name]]</span>
                    </div>
                    <div class="main-cart-item-number">
                        <div class="item-info-price-quantity">
                            <p v-on:click="delQt(index)">-</p><input style="background: transparent; color:#e63d44 " id="quantity" readonly type="number" :value="[[item.num]]" min="1"><p v-on:click="addQt(index)">+</p>
                        </div>
                    </div>
                    <div class="main-cart-item-price">[[item.price]] <i class="fa fa-rub"></i></div>
                    <div class="main-cart-item-total-price">[[item.num * item.price]] <i class="fa fa-rub"></i></div>
                    <div class="main-cart-item-action"><span class="cart-delete-btn" v-on:click="userDelete(index)">&#10006;</span></div>
                </div>`,

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
        selectedSize:null,
        selectedSizeName:'Выберите цвет',
        selectedHeight:null,
        selectedHeightName:'Выберите цвет',
        sizes:null,
        heights:null,
        coords: [54.82896654088406, 39.831893822753904],
        cartTotal:0,
        cartItemsNum:0,
        cartNotEmpty : false,
        sidePanelActive:false,
        mobileCatalogActive:false,
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
            this.selectedColor = index
            this.sizes = this.itemInfo[index].sizes
            this.heights = this.itemInfo[index].heights
            this.selectedSizeName = 'Выберите размер'
            this.selectedHeightName = 'Выберите размер'

            console.log('this.sizes',this.sizes)
            console.log('this.heights',this.heights)

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
        addItem: function (event) {
            let item_id = event.target.getAttribute('data-id'),
                item_name = event.target.getAttribute('data-name'),
                item_price = event.target.getAttribute('data-price'),
                item_image = event.target.getAttribute('data-image')

            console.log('add')
            this.headerCartItems.push({id:item_id,name:item_name,price:item_price,num:1,image:item_image })
            event.target.innerText='в корзине'
            event.target.setAttribute('disabled','disabled')
            this.sendUpdateRequest(item_id,'add_new')
            Toastify({
                duration: 1000,
                close: true,
                text: `${item_name} добавлен в корзину`,
                backgroundColor: "linear-gradient(to right, #f55f63, #be353b)",
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
            this.cartTotal = 0
            let x = 0,
                cart_items_count = document.getElementById('cart_items_count')

            for(var item in val){
                console.log(val[item]['price'])
                this.cartTotal +=  parseInt(val[item]['price']) * parseInt(val[item]['num'])
                x+=1
            }
            console.log('items count=', x)
            this.cartItemsNum = x
            if (x === 0){
                cart_items_count.classList.add('empty')
            }else{
                 cart_items_count.classList.remove('empty')
            }
        }
    }
})
