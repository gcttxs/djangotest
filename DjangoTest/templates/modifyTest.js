function myConnect1(){
    jQeury.get("#i1").val();
    console.log(jQeury.get("#i1").val());
    $.post('127.0.0.1:8000/connectTest',{'url':url},function(res){
        console.log(res)
    })

}