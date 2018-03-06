$(document).ready(function(){
  $("#login-button").click(function(){
    $('#form').fadeOut("slow",function(){
      $(this).remove();
      $("#anim-left").animate({width:'-=100%',height:'-=100%'},5000,"linear",function(){$(this).remove();});
      $("#anim-up").animate({width:'-=100%',height:'-=100%'},5000,"linear",function(){$(this).remove();});
      $("#anim-right").animate({width:'-=100%',height:'-=100%'},5000,"linear",function(){$(this).remove();});
      $("#anim-down").animate({width:'-=100%',height:'-=100%'},5000,"linear",function(){$(this).remove();});
      
    });
  });
});
