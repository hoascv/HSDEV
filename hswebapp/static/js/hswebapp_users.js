$(document).ready(function() {

    $('.updateButton').on('click', function() {
        
        var user_id     = $(this).attr('member_id');
        var username    = $('#nameInput'+user_id).val();
        var email       = $('#emailInput'+user_id).val();
        
        req = $.ajax({
            url : '/update_user',
            type : 'POST',
            data : { username : username, email : email, id : user_id }
        });

        req.done(function(data) {
            if (data.result=='success'){     
                $('#usersection'+user_id).fadeOut(1000).fadeIn(1000);
                $('#response'+user_id).css('color','blue');
                $('#updatedAt'+user_id).val(data.updated);    
            }
            else
                alert('Error updating the user');
            
        });

    });

    setInterval(function(){

        $('#teste').fadeOut(1000).fadeIn(1000);}, 2000);     
});