$(".dropdown-menu li a").click(function(){
  
  $("#taskbtn").html($(this).text()+' <span class="caret"></span>');

  $("input[name='task']").val($(this).text());
});

// function toggleCheckboxes() {  
//   const masterCheckBox = $("input[type='hidden'].master"); 
//   masterCheckBox[0].val=!masterCheckBox[0].val;
//   const checkboxes = $("input[type='checkbox']");    
//   const isMasterChecked = masterCheckBox[0].val;
//   for(var i=0; i<checkboxes.length; i++) {
//     console.log(checkboxes[i]); 
//     checkboxes[i].checked = isMasterChecked;
//   }
// } 
