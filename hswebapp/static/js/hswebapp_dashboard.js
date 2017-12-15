var update_pool=2000;    

$(document).ready(function() {

    
    google.charts.load('current', {'packages':['gauge']});
    google.charts.setOnLoadCallback(drawChartTemp1);
    google.charts.setOnLoadCallback(drawChartTemp2);
    google.charts.setOnLoadCallback(drawChartTemp3);
	google.charts.setOnLoadCallback(drawChartHum1);
    google.charts.setOnLoadCallback(drawChartHum2);
	google.charts.setOnLoadCallback(drawChartPressure);
    google.charts.setOnLoadCallback(drawChartPower);
	   
    function drawChartTemp1() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp ºC', parseInt($('#temperature_sensor1value').text())]
         
        ]);

        var temp_options = {
		  min: -10, max: 50,
          width: 440, height: 132,
		  greenFrom:20, greenTo:30,
          redFrom: 35, redTo: 50,
          yellowFrom:30, yellowTo: 35,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_temp1_div'));
		chart.draw(data, temp_options);    
        
    } 
    function drawChartTemp2() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp ºC', parseInt($('#temperature_sensor2value').text())]
         
        ]);

        var temp_options = {
		  min: -10, max: 50,
          width: 440, height: 132,
		  greenFrom:20, greenTo:30,
          redFrom: 35, redTo: 50,
          yellowFrom:30, yellowTo: 35,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_temp2_div'));
		chart.draw(data, temp_options);    
        
      } 
 
 
    function drawChartTemp3() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temp ºC', parseInt($('#temperature_sensor3value').text())]
         
        ]);

        var temp_options = {
		  min: -10, max: 50,
          width: 440, height: 132,
		  greenFrom:20, greenTo:30,
          redFrom: 35, redTo: 50,
          yellowFrom:30, yellowTo: 35,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_temp3_div'));
		chart.draw(data, temp_options);    
        
      }
    function drawChartHum1() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humidity %', parseInt($('#humidity_sensor1value').text())]
        ]);

        var humidity_options = {
		  min: 0, max: 100,
          width: 440, height: 132,
		  greenFrom:30, greenTo:50,
          redFrom: 50, redTo: 100,
          
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_humidity1_div'));
		chart.draw(data, humidity_options);    
        
      }
    
    function drawChartHum2() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humidity %', parseInt($('#humidity_sensor2value').text())]
        ]);

        var humidity_options = {
		  min: 0, max: 100,
          width: 440, height: 132,
		  greenFrom:30, greenTo:50,
          redFrom: 50, redTo: 100,
          
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_humidity2_div'));
		chart.draw(data, humidity_options);    
        
      }
    function drawChartPressure() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Pressure hPa', parseInt($('#pressure_sensor1value').text())]
        ]);

        var pressure_options = {
		  min: 960, max: 1040,
          width: 440, height: 132,
		  greenFrom:20, greenTo:30,
          redFrom: 35, redTo: 50,
          yellowFrom:30, yellowTo: 35,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_pressure_div'));
		chart.draw(data, pressure_options);    
        
     }	           
     function drawChartPower() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['mVolts', parseInt($('#power_sensor1value').text())]
        ]);

        var power_options = {
		  min: 0, max: 6000,
          width: 440, height: 132,
		  greenFrom:5000, greenTo:6000,
          redFrom: 0, redTo: 4499,
          yellowFrom:4500, yellowTo: 4999,
          minorTicks: 100
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_power_div'));
		chart.draw(data, power_options);    
        
      }  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    setInterval(function(){
        var new_value=0
        
        req = $.ajax({
            url : '/update_dashboard',
            type : 'GET'
            
        });

        req.done(function(data) {
           
            
            if (data.result!='noresult'){     
                
                //$('#usersection'+user_id).fadeOut(1000).fadeIn(1000);
                //$('#response'+user_id).css('color','blue');
                //$('#updatedAt'+user_id).val(data.updated); 
                
                $('#hsousa').text("last update sensor: "+data.sensor + " value:"+ data.voltage + ' date: ' + data.rdate+ "  TYPE:"+data.type_data);
                
                //$('#sensor1value').text(data.value);
                if (data.type_data=='PowerLog'){
                    new_value =parseInt(data.voltage)*1000;          
                    $('#'+data.sensor+'value').text(new_value);
                }    
                else {
                     
                    new_value =parseInt(data.value);          
                    $('#'+data.sensor+'value').text(new_value);
                }
            }   
            else{
                  $('#hsousa1').text(data.result);
            }
                
        drawChartTemp1();
        drawChartTemp2();
        drawChartTemp3();
        drawChartHum1(); 
        drawChartHum2();
        drawChartPressure();
        drawChartPower();
        });

    },update_pool);     

        
        
        
        
});