<div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3>Add Repository</h3>
</div>

<form class="form-horizontal" data-ng-submit="addRepo(dismiss)">
    <div class="modal-body">
        <p>Leave the <strong>path</strong> empty and a new directory will be created.</p>

        <div class="control-group">
            <label class="control-label" for="upstream">Upstream</label>
            <div class="controls">
                <input type="text" id="upstream" placeholder="Upstream" required data-ng-model="upstream">
            </div>
        </div>
        <div class="control-group">
            <label class="control-label" for="path">Path</label>
            <div class="controls">
                <input type="text" id="path" placeholder="Path" data-ng-model="path">
            </div>
        </div>
    </div>

    <div class="modal-footer">
        <p class="pull-left" data-ng-show="error">{{error}}</p>

        <button type="button" class="btn" ng-click="dismiss()">Close</button>
        <button class="btn btn-primary" type="submit">Add</button>
    </div>
</form>
