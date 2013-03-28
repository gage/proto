var BigPipe = {
    ready: false,
    start: function(){
        this.ready = true;
        for(var i=0,len=this.queue.length;i<len;i++){
            this.process(this.queue[i]);
        };
    },
    queue: new Array(),
    process: function(jsonData){
        var css_files = _.map(jsonData.css_files, function(file){
            return 'css!css_root/'+file.split('.css')[0];
        });
        //require css resources
        require(css_files , function(){
            //inject html
            $('#'+jsonData.id).html(jsonData.innerHTML);
            //js init
            require([jsonData.jsModuleFile], function(){});
        });
    },
    onArrive: function(jsonData){
        if(this.ready){
            this.process(jsonData);
        }else{
            this.queue.push(jsonData);
        };
    }
};