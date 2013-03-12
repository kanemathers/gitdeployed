angular.module('gitdeployed.services', [
    'ngResource'
])

.factory('Repos', [
    '$resource',

    function($resource)
    {
        return $resource('/repos/:repoId', {repoId: '@id'});
    }
]);
