define(['jquery',
        'underscore', 
        'backbone',
        'site/site'], 
function($, _, Backbone, Site) {
    describe("test Site.exampleFun", function() {
        var foo, bar;
        beforeEach(function() {
            foo = 3;
            bar = 4
        });

        it ("example: add", function() {
            var results = Site.exampleFun(foo, bar);
            expect(results).toEqual(12);
        });

        it ("example: this should raise error", function() {
            var results = Site.exampleFun(foo, bar);
            expect(results).toEqual(0);
        });
    });
});    