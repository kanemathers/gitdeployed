angular.module('gitdeployed.services', [
    'ngResource'
])

.factory('Repos', [
    '$http',
    '$resource',

    function($http, $resource)
    {
        return $resource('/repos/:repoId', {repoId: '@id'});
    }
]);
