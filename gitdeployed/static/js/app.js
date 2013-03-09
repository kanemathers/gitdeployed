angular.module('gitdeployed', [
    'gitdeployed.controllers',
    'gitdeployed.services',
    '$strap.directives'
])

.config([
    '$routeProvider',

    function($routeProvider)
    {
        $routeProvider
            .when('/repos', {
                controller:  'ReposCtrl',
                templateUrl: '/partials/repos.html'
            })
            .when('/config', {
                controller:  'ConfigCtrl',
                templateUrl: '/partials/config.html'
            })

            .otherwise({redirectTo: '/repos'});
    }
]);
