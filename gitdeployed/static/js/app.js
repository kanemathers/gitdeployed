angular.module('gitdeployed', [
    'gitdeployed.controllers',
    'gitdeployed.services',
    'gitdeployed.directives',
    '$strap.directives'
])

.config([
    '$routeProvider',
    '$httpProvider',

    function($routeProvider, $httpProvider)
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

        var interceptor = [
            '$rootScope',
            '$q',

            function($rootScope, $q)
            {
                var success = function(response)
                {
                    return response;
                };

                var error = function(response)
                {
                    if (response.status != 403)
                        return $q.reject(response);

                    var deferred = $q.defer();
                    var request  = {
                        config:   response.config,
                        deferred: deferred
                    };

                    $rootScope.requestQueue.push(request);
                    $rootScope.$broadcast('auth:required');

                    return deferred.promise;
                };

                return function(promise)
                {
                    return promise.then(success, error);
                };
            }
        ];

        $httpProvider.responseInterceptors.push(interceptor);
    }
])

.run([
    '$rootScope',
    '$http',

    function($rootScope, $http)
    {
        $rootScope.requestQueue = [];

        var retry = function(request)
        {
            $http(request.config).then(function(response)
            {
                request.deferred.resolve(response);
            });
        };

        $rootScope.$on('auth:success', function()
        {
            angular.forEach($rootScope.requestQueue, function(request)
            {
                retry(request);
            });
        });
    }
]);
