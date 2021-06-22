

//Function for remove product from cart_page
  $('.remove-cart').click(function(){
    var id = $(this).attr('productid').toString();
    console.log('Product id::', id)
    node = this
    $.ajax({
      url:'/site_app/delete',
      type:'GET',
      data:{
        pid:id
      },
      success:function(data){
        //document.getElementById('remove').remove()
        node.parentNode.parentNode.remove()
        document.getElementById('subtotal').innerText = (data.sum)
        document.getElementById('shipcharg').innerText = (data.shipcharg)
        document.getElementById('total').innerText = (data.total)
      }
    })
  })

  //Function for remove product from checkout_page
  $('.remove-item').click(function(){
    var id = $(this).attr('productid').toString();
    console.log('Product ID = ', id)
    node = this
    $.ajax({
      url:'/site_app/delete',
      type: 'GET',
      data:{
        pid:id
      },
      success:function(data){
        console.log('Message::', data.message)
        node.parentNode.parentNode.parentNode.remove()
        document.getElementById('subtotal').innerText = (data.sum)
        document.getElementById('shipcharg').innerText = (data.shipcharg)
        document.getElementById('total').innerText = (data.total)
      }
    })
  })

// Function for increment product
$('.plus-cart').click(function(){
  var id = $(this).attr('productid').toString()
  var forspantag = this.parentNode.children[1]
  var forquantitytotaltag = this.parentNode.parentNode.children[3]
  console.log('Plus Product Id = ',  id)
  $.ajax({
    url:'/site_app/pluscart',
    type:'GET',
    data:{
      prod_id:id
    },
    success:function(data){
      console.log("Product Quantity::", data.quantity)
      forspantag.innerText = data.quantity
      forquantitytotaltag.innerText = data.total_amount
      document.getElementById('subtotal').innerText = (data.sum)
      document.getElementById('shipcharg').innerText = data.ship_charg
      document.getElementById('total').innerText = (data.total).toLocaleString('en-US', {style: 'currency', currency: 'INR', });

      //console.log('Sub Total::', data.sum)
      //console.log('Total with shipcharg: ', data.total)
      //console.log('Product Amount: ', data.amount)
      //console.log('Product Ship Charg: ', data.ship_charg)
      //console.log('Quantity Amount: ', data.quantity_amount)
      //console.log('Product Amount: ', data.total_amount)
    }
  });
})

  $('.minus-cart').click(function(){
    var id = $(this).attr('productid').toString()
    console.log('Minus Product Id = ', id)
    var forspantag = this.parentNode.children[1]
    var forquantitytotaltag = this.parentNode.parentNode.children[3]
    $.ajax({
      url:'/site_app/minuscart',
      type:'GET',
      data:{
        prod_id:id
      },
      success:function(data){
        console.log('Product Quantity:::', data.quantity)
        forspantag.innerText = data.quantity
        forquantitytotaltag.innerText = data.total_amount
        document.getElementById('subtotal').innerText = (data.sum)
        document.getElementById('shipcharg').innerText = data.ship_charg
        document.getElementById('total').innerText = (data.total).toLocaleString('en-US', {style: 'currency', currency: 'INR', });
          //console.log('Sub Total::', data.sum)
          //console.log('Total with shipcharg:: ', data.total)
          //document.getElementById('total').innerText = data.total_amount
          // console.log('Product Amount: ', data.amount)
          // console.log('Product Ship Charg: ', data.ship_charg)
          // console.log('Quantity Amount: ', data.quantity_amount)
          // console.log('Product Amount: ', data.total_amount)
          //document.getElementById('myspan').innerText = data.quantity
      }
    });
  })
