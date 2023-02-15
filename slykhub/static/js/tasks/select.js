
$(document).ready(function (){
    var table = $('#taskstable');
  
   // Handle click on "Select all" control
   $('#example-select-all').on('click', function(){
    // Get all rows with search applied
   //  var rows = table.rows({ 'search': 'applied' }).nodes();
   var rows = table.rows({ page: 'current' }).nodes();
   const checkboxes = $("input[type='checkbox']");
   var aux1=0;
   var aux2=0;
   for(var i=0; i<checkboxes.length; i++) {
     if(checkboxes[i].checked){
         aux1+=1;
         console.log(aux1);
     }
     else{
      aux2+=1;
      console.log(aux2);
     }
   }
   var valueToMaster = (aux1<aux2);
   console.log(valueToMaster, aux1, aux2);
    // Check/uncheck checkboxes for all rows in the table
    var masterCheckBox = $("input[type='hidden'].master");
    masterCheckBox[0].val=valueToMaster;
   //  masterCheckBox[0].val=!masterCheckBox[0].val;
    var isMasterChecked = masterCheckBox[0].val;
    var info = table.page.info();
    console.log(info['page']);
    $('input[type="checkbox"]', rows).prop('checked', isMasterChecked);
  });
  
  // Handle click on checkbox to set state of "Select all" control
  $('#taskstable tbody').on('change', 'input[type="checkbox"]', function(){
    var masterCheckBox = $("input[type='hidden'].master");
    // If checkbox is not checked
    if(!this.checked){
       var el = masterCheckBox.get(0);
       // If "Select all" control is checked and has 'indeterminate' property
       if(el && el.checked && ('indeterminate' in el)){
          // Set visual state of "Select all" control
          // as 'indeterminate'
          el.indeterminate = true;
       }
    }
  });
    // Handle form submission event
    $('#tasksform').on('submit', function(e){
      var form = this;
  
      // Iterate over all checkboxes in the table
      table.$('input[type="checkbox"]').each(function(){
         // If checkbox doesn't exist in DOM
         if(!$.contains(document, this)){
            // If checkbox is checked
            if(this.checked){
               // Create a hidden element
               $(form).append(
                  $('<input>')
                     .attr('type', 'hidden')
                     .attr('name', this.name)
                     .val(this.value)
               );
            }
         }
      });
   });
   
   if ( ! $.fn.DataTable.isDataTable( table) ) {
      table = table.DataTable();
      console.log('isDataTable');
    }
    
  });
  