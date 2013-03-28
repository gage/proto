({
    baseUrl: '.',
    paths: {
        lib: 'lib',
        jquery: 'lib/jquery-min',
        backbone: 'lib/backbone-min',
        underscore: 'lib/underscore-min',
        less: 'lib/less'
    },
    name: 'main',
    out: 'main-built.js',
    shim: {
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        underscore: {
            exports: '_'
        },
    },
    map: {
        '*': {
            'css': 'lib/require-css/css'
        }
    }
})