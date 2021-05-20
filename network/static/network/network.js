$('.likebutton').click(function(){
    var catid;
    var total;
    var value;
    catid = $(this).data("catid");
    

    $.ajax(
    {
        type:"GET",
        url: "/likepost",
        data:{
                post_id: catid
        },
        success: function( data ) 
        {
            total = $('#'+ catid).attr("data-total")
            if ($('#'+catid).attr("data-value") == 'Like'){
                $( '#liked'+catid ).text((parseInt(total) + 1));
                $( '#heart'+catid ).css('color', 'red')
                $('#'+catid).attr("data-total", parseInt(total) + 1)
                $('#'+catid).attr("data-value", 'Unlike')
            }
            else{
                $( '#liked'+catid ).text((parseInt(total) - 1));
                $( '#heart'+catid ).css('color', 'black')
                $('#'+catid).attr("data-total", parseInt(total) - 1)
                $('#'+catid).attr("data-value", 'Like')
            }
        }
    })

    
})

$(function() {
    $( 'a[href$="#"]' ).each(function() {
        $( this ).attr( 'href','javascript:void(0);' )
        });
    });
$(".expand-button").click(function() {
$("#profile").toggleClass("expanded");
$("#contacts").toggleClass("expanded");
});
$("#profile-img").click(function() {
$("#status-options").toggleClass("active");
});

        document.addEventListener('DOMContentLoaded', () => {



   

      
        fetch('/network/posts')
        .then(response => response.json())
        .then(posts => {
            console.log(posts)
            for(i in posts){
                
                const clas=posts[i].id
                const user=posts[i].user
                const cont=posts[i].content

                let div=document.createElement('div')
                div.setAttribute("class","class-post")
                
                let form=document.createElement('form')
                
        
                let button=document.createElement('button')
                button.setAttribute("class","save btn btn-outline-dark")
               
                button.setAttribute("value","save")
        
                let b=document.createElement("i")
                b.setAttribute("class","fa fa-floppy-o")
        
                let br=document.createElement("br")
        
                let textar=document.createElement("textarea")
                textar.innerHTML=`${cont}`
                button.setAttribute("disabled","true")
                textar.setAttribute("class","edit_area")
        
                button.innerHTML+=b.outerHTML+"save"
                form.innerHTML+=textar.outerHTML+  br.outerHTML+button.outerHTML

              

       
        

                
              
               
                $(`.edit${clas}`).click(function(){
                   
              
                    $(`#edit_textarea${clas}`).html(form.outerHTML);
                     // Enable button only if there is text in the input field
           
                     document.querySelector('.edit_area').onkeyup = () => {
                        if (document.querySelector('.edit_area').value.length > 0)
                            document.querySelector('.save').disabled = false;
                        else
                            document.querySelector('.save').disabled = true;
                            };
        
                  
                    document.querySelector(".save").onclick=()=>{
                    
                        const content=document.querySelector('.edit_area').value
                       
        
                        let content_area=document.createElement("p")
                        content_area.setAttribute("class","card-text")
                        content_area.innerHTML=content
        
                        let br=document.createElement('br')
        
                        let button=document.querySelector('button')
                        button.setAttribute("id","edit_button")
                        button.setAttribute("class",`.edit${clas}`)
                        let i=document.createElement('i')
                        i.setAttribute("class","fa fa-edit")
                        button.innerHTML="Edit"+i.outerHTML

                        fetch(`/network/posts/${clas}`, {
                            method: 'POST',
                            body: JSON.stringify({
                                user: user,
                               
                                body: content
                            })
                          })
                          .then(response => response.json())
                          .then(result => {
                              // Print result
                              console.log(result);
                          });
        
                      
        
                        $(`#edit_textarea${clas}`).html(content_area.outerHTML+br.outerHTML+button.outerHTML); 

                 
        
        
        
        
                    }
                })

            }
        })
          



    });