$(document).ready(function() {
    
    var my_loop;
    
    var repeat_request_temp = false;
    var repeat_request_hum = false;
    var repeat_request_pre = false;
    
    
    var sucess_requests =0;
    var error_requests=0;
    
    
    var infoTemperatureLog_sucess_request =0;
    var infoTemperatureLog_error_request=0;
    
    var infoHumidityLog_sucess_request =0;
    var infoHumidityLog_error_request=0;
    
    var infoPressureLog_sucess_request =0;
    var infoPressureLog_error_request=0;
    
    
    var speed=10;
    var sensor_url_temp="";
    var sensor_url_hum="";
    var sensor_url_pre="";
    var request_id=0;
    
    var request; // object request 
    var temp_request_done=true;
    var hum_request_done=true;
    var pre_request_done=true;
    
    
    
        
    my_loop = window.setInterval(function(){
        
        if (repeat_request_temp && temp_request_done){
            temp_request_done=false;
            repeatRequest(sensor_url_temp,'TempLog');      
        }
        
        if (repeat_request_hum && hum_request_done){
            hum_request_done=false;
            repeatRequest(sensor_url_hum,'HumidityLog');
        }    
       
        if (repeat_request_pre && pre_request_done){
            pre_request_done=false;
            repeatRequest(sensor_url_pre,'PressureLog');
        }    
                
    },speed);
    
       
    
    $('#btnTemperature').on('click', function() {
      speed=parseInt(parseInt($('#speed').val()));
      option='TempLog';
      sensor_url_temp='?sensor_type='+option;
     
      
     if (repeat_request_temp){
        repeat_request_temp= false;
        $('#btnTemperature').text('Resume Update');
        
       
        
           
     
     }     
     else {
        repeat_request_temp= true
        $('#btnTemperature').text('Cancel Update');
        
     }         
      
    
    
    });
    
    $('#btnHumidity').on('click', function() {
      speed=parseInt(parseInt($('#speed').val()));
      option='HumidityLog';
      sensor_url_hum='?sensor_type='+option;
      
      
     if (repeat_request_hum){
        repeat_request_hum= false;
        $('#btnHumidity').text('Resume Update');
        
       
        
           
     
     }     
     else {
        repeat_request_hum= true
        $('#btnHumidity').text('Cancel Update');
        
     }         
      
    
    
    });
    
    $('#btnPressure').on('click', function() {
      speed=parseInt(parseInt($('#speed').val()));
      option='PressureLog';
      sensor_url_pre='?sensor_type='+option;
      
      
     if (repeat_request_pre){
        repeat_request_pre= false;
        $('#btnPressure').text('Resume Update');
        
     }     
     else {
        repeat_request_pre= true
        $('#btnPressure').text('Cancel Update');
        
     }         
      
       
    });
    
    
    
    function repeatRequest(sensor_url,option){
    
    
    request_id=request_id+1;
    request = {'request_id':request_id,
                   'sensor_url':sensor_url,
                   'temp_request_done':false,
                   'hum_request_done':false,
                   'pre_request_done':false};
                   
    req = $.ajax({
            url : '/exporting_templog'+sensor_url,
            type : 'GET',
            //data : { username : username, email : email, id : user_id }
            
            statusCode: {
                404: function() {
                        alert( "route not found" );
                    },
                409: function() {
                        error_requests=error_requests+1;
                    },
                201: function() {
                        sucess_requests=sucess_requests+1;
                    },    
               
                503: function() {
                        error_requests=error_requests+1;
                    },    
                   
               
                422: function() {
                        error_requests=error_requests+1;
                    },
                204: function() {
                        repeat_request=false;
                        
                    }                                                
                    
            },
            
            success: function(data, textStatus, XMLHttpRequest) {
                                                                 onGetResourceResponse(data, textStatus, XMLHttpRequest)},
            error: function(XMLHttpRequest, textStatus, errorThrown){
                                                                onGetResourceError(XMLHttpRequest, textStatus, errorThrown)}                                                     
    });
    req.type=option;
    req.req_id=request_id;
    req.req=request;
    }
     
     function onGetResourceResponse(data, textStatus, XMLHttpRequest){
    
    //if(XMLHttpRequest.uniqueId) {
      // console.log(XMLHttpRequest.req_id);
       console.log(XMLHttpRequest.req['request_id']);
       
       console.log(XMLHttpRequest.req['sensor_url']);
       
      //}
      
     if (XMLHttpRequest.type==='TempLog' ){
        temp_request_done=true; 
        infoTemperatureLog_sucess_request=infoTemperatureLog_sucess_request+1;
        if (XMLHttpRequest.status===204){
            repeat_request_temp=false;
            
            $('#btnTemperature').text('Resume Update');
        }
        $('#infoTemperatureLog_sucess_request').text(infoTemperatureLog_sucess_request);
        
      } else if (XMLHttpRequest.type==='HumidityLog'){
             hum_request_done=true;   
             infoHumidityLog_sucess_request=infoHumidityLog_sucess_request+1;  
             if (XMLHttpRequest.status===204){
                    repeat_request_hum=false;
                    $('#btnHumidity').text('Resume Update');
             }   



        $('#infoHumidityLog_sucess_request').text(infoHumidityLog_sucess_request);   
        } 
      else if (XMLHttpRequest.type==='PressureLog'){
        pre_request_done=true;
        infoPressureLog_sucess_request=infoPressureLog_sucess_request+1;
        
            if (XMLHttpRequest.status===204){
                 repeat_request_pre=false;
                 $('#btnPressure').text('Resume Update');
             }   
        
        
        $('#infoPressureLog_sucess_request').text(infoPressureLog_sucess_request);
      }
      else {
          
          alert(XMLHttpRequest.type + "not defined");
      }

      request_done_refresh();
    }

     function onGetResourceError(XMLHttpRequest, textStatus, errorThrown){
    
    
       console.log(XMLHttpRequest.req['request_id']);
      
      if (XMLHttpRequest.type==='TempLog'){
          temp_request_done=true;
        infoTemperatureLog_error_request=infoTemperatureLog_error_request+1;
        $('#infoTemperatureLog_error_request').text(infoTemperatureLog_error_request);    
      } 
        else if (XMLHttpRequest.type==='HumidityLog'){
            hum_request_done=true;
            infoHumidityLog_error_request=infoHumidityLog_error_request+1;
            $('#infoHumidityLog_error_request').text(infoHumidityLog_error_request);      
      } 
        else if (XMLHttpRequest.type==='PressureLog'){
            pre_request_done=true;
            infoPressureLog_error_request=infoPressureLog_error_request+1;
            $('#infoPressureLog_error_request').text(infoPressureLog_error_request);
      }
      else {
          alert(XMLHttpRequest.type + "not defined");
      }
      request_done_refresh();
      
    
    }

    function request_done_refresh(){
        if ( !repeat_request_temp && !repeat_request_hum && !repeat_request_pre){
            location.reload();     
        }   
    }     
  
    

  
});