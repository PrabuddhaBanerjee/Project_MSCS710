$(function(){
   var $date = $('#checkDate');
   var $graphDate = $('#getDate');
   var $flightDate = $('#start');
  //Best Airport Available
   $('#generate-ports').on('click',function(){
     var dates = $date.val();
     var date_sp = dates.split("-");
     if(date_sp[0]>2017){
        var year = 2016;
     }
     else if(date_sp[0]<2013){
        var year = 2013;
     }
     else var year = parseInt(date_sp[0]);
    var month = parseInt(date_sp[1]);
    if(date_sp[1].charAt(0)=="0")
      month = parseInt(date_sp[1].charAt(1));
    var dt = parseInt(date_sp[2]);
    if(date_sp[2].charAt(0)=="0")
      dt = parseInt(date_sp[2].charAt(1));
     var travelOn = {
        "year" : year,
        "month": month,
        "day": dt
     };
           $.ajax({
          type:'POST',
          url:'http://localhost:8080/csumano/AIRservices/1.0.0/bestairlines',
          contentType: "application/json",
          data: JSON.stringify(travelOn),
          success: function(airport){
            // alert(airport);
            var rawData = airport;
            var dataPorts = rawData.split("},");
            // alert(dataPorts[0]+"@@@@@@");
            // alert(dataPorts[1]);
            var set_port = dataPorts[0].split("ORIGIN_CITY_NAME");
            var origins = set_port[1].replace(/[^a-zA-Z, ]/g,'');
            var set_city = dataPorts[1].split("ORIGIN");
            var departs = set_city[1].replace(/[^a-zA-Z, ]/g,'');
            var set_arrive = dataPorts[2].split("RELIABILITY");
            // alert(set_arrive[1]);
            var arrive = set_arrive[1].replace(/[^0-9.:]/g,'');
            //  alert("origins:"+origins);
            // alert("arrive:"+arrive);
            var printOrigin = origins.split(",");
            var printOriginCity = departs.split(",");
            var printArrive = arrive.split(":");
            //  alert(printOrigin+" "+printOrigin.length);
            // alert(printArrive+" "+printArrive.length);
            var i,j;
            j=0;
            for( i=0; i<20; i=i+2){
                
                // alert(i+" "+printOrigin[i]+"@@"+printArrive[i+2]+"@@"+origins);
                if(parseFloat(printArrive[j+2])<100){
                  var newElement = '<tr><td>'+printOrigin[i]+","+printOrigin[i+1]+'</td><td style="text-align: center;">'+printOriginCity[j]+'</td><td style="text-align: center;">'+parseFloat(printArrive[j+2]).toFixed(4)+'%</td><td></tr>';
                }
                else 
                var newElement = '<tr><td>'+printOrigin[i]+","+printOrigin[i+1]+'</td><td style="text-align: center;">'+printOriginCity[j]+'</td><td style="text-align: center;">100%</td><td></tr>';
                $( "#mytable" ).append( $(newElement));
                j++
              }
            // alert("till here");
          },
          error: function(){
            alert('Data for the given dates are not found');
          }
      });
   });
   //
   $('#generate-flight').on('click',function(){
    //  alert("In2");
    var dates = $flightDate.val();
    var date_sp = dates.split("-");
     if(date_sp[0]>2017){
        var year = 2016;
     }
     else if(date_sp[0]<2013){
        var year = 2013;
     }
     else var year = parseInt(date_sp[0]);
    var month = parseInt(date_sp[1]);
    if(date_sp[1].charAt(0)=="0")
      month = parseInt(date_sp[1].charAt(1));
    var dt = parseInt(date_sp[2]);
    if(date_sp[2].charAt(0)=="0")
      dt = parseInt(date_sp[2].charAt(1));
    var depart  = $("#getDepart :selected").val();
    var arrival = $("#getArrive :selected").val();
    // alert(depart+" "+arrival);
    if((depart == arrival)&&(depart!="--Choose an Option--")&&(arrival!="--Choose an Option--"))
      return alert("The Arrival and Departure can't be same");
    var data_obj = {
       "day" : dt,
       "destination": arrival,
       "month": month,
       "origin": depart,
       "year": year
    };
    // alert(data_obj.day);
    model = "Ensembled"
    $.ajax({
         type:'POST',
         url:'http://localhost:8080/csumano/AIRservices/1.0.0/flightpredictor?Model='+model,
         contentType: "application/json",
         data: JSON.stringify(data_obj),
         success: function(flights){
          //  alert(flights);
           var data = flights.split(",");
           var cancel = data[0].split(":");
           var delay = data[1].split(":");
           var newElement = '<tr><td style="text-align: center;">'+parseFloat(cancel[1]).toFixed(4)+'%</td><td style="text-align: center;">'+parseFloat(delay[1]).toFixed(4)+'%</td><td></tr>';
           $( "#myFlight" ).append( $(newElement));
         },
         error: function(){
           alert('Data for the given dates are not found');
         }
     });
  });
  // Flight Graph
   $('#generate-graph').on('click',function(){

        var condition  = $("#getCondition :selected").text();

        var dates = $graphDate.val();

        var date_sp = dates.split("-");
         
        if(date_sp[0]>2017){
            var year = 2016;
        }
        else if(date_sp[0]<2013){
            var year = 2013;
        }
        else var year = parseInt(date_sp[0]);
         
      $.ajax({
            type:'GET',
            url:'http://localhost:8080/csumano/AIRservices/1.0.0/flightgraphs?Graph='+condition+'&Year='+year,
            contentType: "text/html",
            success: function(graph){
                graph_url = 'http://localhost:8080/csumano/AIRservices/1.0.0/flightgraphs?Graph='+condition+'&Year='+year;
//                 alert(graph_url);
                window.open(graph_url, '_blank');
                if (win) {
                  //Browser has allowed it to be opened
                  win.focus();
              } else {
                  //Browser has blocked it
                  alert('Please allow popups for this website');
              }
            },
            error: function(){
              alert('Data for the given dates are not found');
            }
      });
  });
});
