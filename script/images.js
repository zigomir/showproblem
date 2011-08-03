$(document).ready(function(){
    // init
	var currentImage = $('.images > img').first().attr('id');
    var firstImage = $('.images > img').first().attr('id');
    var lastImage = $('.images > img').last().attr('id');
    
    // create each image link
    $('.images > img').each(function(i){
    	id = $(this).attr('id');
    	
    	delimit = ' | ';
    	if (id == lastImage)
    		delimit = '';
    	
    	$('.imageWalk').append('<a id="step" href="#' + id + '">Step ' + id + '</a><a>' + delimit + '</a>');
    	
    	// after every 15 steps do newline
    	if (parseInt(id) % 15 == 0)
    		$('.imageWalk').append('<br/>');
    });
    
    renderImage();
    
    function renderImage(){
        $('.images > img').hide();
        $('.images > img[id="' + currentImage+ '"]').show();
        
        $('.imageWalk > a').css('color', 'blue');
        $('.imageWalk > a').css('font-size', '0.7em');
        
        $('.imageWalk > a[href="#' + currentImage + '"]').css('color', 'red');
        $('.imageWalk > a[href="#' + currentImage + '"]').css('font-size', '0.9em');
    }
    
    $('a#step').click(function(event){
    	event.preventDefault();
    	var parts = this.href.split('#');
        currentImage = parts[1];
        renderImage();
    });
    
    $('a#next').click(function(event){
        event.preventDefault();
        if (!preventCurrentImageIncrement()){
            currentImage++;
        }
        renderImage();
    });
    
    $('a#prev').click(function(event){
        event.preventDefault();
        if (!preventCurrentImageDecrement()){
            currentImage--;
        }
        renderImage();
    });
    
    function preventCurrentImageDecrement(){
        return currentImage == firstImage ? true : false;
    }
    
    function preventCurrentImageIncrement(){
        return currentImage == lastImage ? true : false;
    }
    
    function checkKey(e){
        switch (e.keyCode) {
            case 37: // left
                if (!preventCurrentImageDecrement()){
                    currentImage--;
                }
                break;
            case 39: // right
                if (!preventCurrentImageIncrement()){
                    currentImage++;
               }
               break;
        }
        renderImage();
    }
    
    if ($.browser.mozilla) {
        $(document).keypress(checkKey);
    }
    else {
        $(document).keydown(checkKey);
    }
});