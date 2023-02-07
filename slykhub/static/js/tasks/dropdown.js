$(".dropdown-menu li a").click(function(){
  
  $(".btn:first-child").html($(this).text()+' <span class="caret"></span>');
  $("input[name='task']").val($(this).text());
});

function toggleCheckboxes(label) {  
  const masterCheckBox = $("input[type='hidden'].master"); 
  if(label){
    masterCheckBox[0].val=!masterCheckBox[0].val;
  }
  const checkboxes = $("input[type='checkbox']");  
  console.log(checkboxes);   
  const isMasterChecked = masterCheckBox[0].val;  
  console.log(checkboxes.length); 
  for(var i=0; i<checkboxes.length; i++) {
    console.log(checkboxes[i]); 
    checkboxes[i].checked = isMasterChecked;
  }
} 

