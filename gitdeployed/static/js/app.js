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

            .otherwise({redirectTo: '/repos'});
    }
]);
