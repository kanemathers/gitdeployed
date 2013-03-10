angular.module('gitdeployed', [
    'gitdeployed.controllers',
    'gitdeployed.services',
    'gitdeployed.directives',
    '$strap.directives'
])

.config([
    '$routeProvider',

    function($routeProvider)
    {
        $routeProvider
            .when('/repos', {
                controller:  'ReposListCtrl',
                templateUrl: '/partials/repos.html'
            })
            .when('/config', {
                controller:  'ConfigCtrl',
                templateUrl: '/partials/config.html'
            })

            .otherwise({redirectTo: '/repos'});
    }
]);
