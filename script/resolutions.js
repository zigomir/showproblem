$(document).ready(function() {
	$('option#full').attr('value', screen.width + 'x' + screen.height);
    $('option#full').html(screen.width + 'x' + screen.height + ' - Fullscreen');
    
    // calculate optimal resolution (one less than full screen)
    var wideScreen1610Ratio = 1.6;
    var wideScreen1610Widths = new Array(2560, 1920, 1680, 1280, 1440);
    var wideScreen1610Heights = new Array(1600, 1200, 1050, 800, 900);
        
    // ratio: 1,77
    var wideScreen169Ratio = 1.77;
    var wideScreen169Widths = new Array(1920, 1280, 1366);
    var wideScreen169Heights = new Array(1080, 800, 768);
    
    // ratio: 1,3
    var nonWideScreenRatio = 1.33;    
    var nonWideScreen43Widths = new Array(2048, 1600, 1400, 1280, 1024, 800);
    var nonWideScreen43Heights = new Array(1536, 1200, 1050, 960, 768, 600);
    
    // ratio: 1,25
    var sxgaRatio = 1.25;
    var sxgaWidths = new Array(2560, 1280, 960);
    var sxgaHeights = new Array(2048, 1024, 768);
    
    var ratio = screen.width / screen.height;
    var optimalWidth = screen.width;
    var optimalHeight = screen.height;
    
    if (ratio.toFixed(2) == wideScreen1610Ratio){
        findOptimalResolution(wideScreen1610Widths, wideScreen1610Heights);
    }
    else if (ratio.toFixed(2) == wideScreen169Ratio){
        findOptimalResolution(wideScreen169Widths, wideScreen169Heights);
    }
    else if (ratio.toFixed(2) == nonWideScreenRatio){
        findOptimalResolution(nonWideScreen43Widths, nonWideScreen43Heights);
    }
    else if (ratio.toFixed(2) == sxgaRatio){
        findOptimalResolution(sxgaWidths, sxgaHeights);
    }
    
    function findOptimalResolution(widths, heights){
        for (var i = 0; i < widths.length; i++){
            if (screen.width == widths[i] && i < widths.length){
                optimalWidth = widths[i + 1];
            }
            if (screen.height == heights[i] && i < heights.length){
                optimalHeight = heights[i + 1];
            }
        }
    }
    
    $('option#optimal').attr('value', optimalWidth + 'x' + optimalHeight );
    $('option#optimal').html(optimalWidth + 'x' + optimalHeight + ' - Optimal');
});