/* Semax workspace boundary selector — behavior only, host owns presentation. */
(function () {
  "use strict";

  var AUTH_BASE = "https://auth.ideanexusventures.com";
  var HANDOFF_KEY = "preview_handoff";

  function removeHandoffFromUrl() {
    var url = new URL(window.location.href);
    url.searchParams.delete(HANDOFF_KEY);
    window.history.replaceState({}, document.title, url.pathname + (url.search ? url.search : "") + url.hash);
  }

  function mount(container, options) {
    options = options || {};
    var authBase = options.authBase || AUTH_BASE;
    var handoff = new URLSearchParams(window.location.search).get(HANDOFF_KEY);
    var selection = null;

    function emit(value) {
      window.dispatchEvent(new CustomEvent("semax:workspace-selected", { detail: value }));
      if (typeof options.onSelect === "function") options.onSelect(value);
    }

    function render() {
      container.replaceChildren();
      if (selection) {
        var selected = document.createElement("span");
        selected.className = "semax-workspace-selector__selected";
        selected.textContent = selection.workspace_id + " / " + selection.property_id;
        container.appendChild(selected);

        var change = document.createElement("a");
        change.className = "semax-workspace-selector__change";
        change.href = authBase + "/workspace/select?return_to=" + encodeURIComponent(window.location.href);
        change.textContent = options.changeLabel || "Change workspace";
        container.appendChild(change);
        return;
      }

      var login = document.createElement("a");
      login.className = "semax-workspace-selector__login";
      login.href = authBase + "/login?return_to=" + encodeURIComponent(window.location.href);
      login.textContent = options.loginLabel || "Sign in to select a workspace";
      container.appendChild(login);
    }

    if (handoff) {
      var loading = document.createElement("span");
      loading.className = "semax-workspace-selector__loading";
      loading.textContent = options.loadingLabel || "Loading workspace…";
      container.replaceChildren(loading);
      removeHandoffFromUrl();
      fetch(authBase + "/preview/redeem?handoff=" + encodeURIComponent(handoff), {
        method: "POST",
        mode: "cors",
        credentials: "omit",
        headers: { "content-type": "application/json" }
      }).then(function (response) {
        if (!response.ok) throw new Error("preview handoff rejected");
        return response.json();
      }).then(function (value) {
        selection = value;
        render();
        emit(value);
      }).catch(function () {
        render();
        if (typeof options.onError === "function") options.onError(new Error("workspace preview could not be established"));
      });
    } else {
      render();
    }

    return {
      getSelection: function () { return selection; },
      clear: function () { selection = null; render(); }
    };
  }

  window.SemaxWorkspaceSelector = { mount: mount };
  document.querySelectorAll("[data-semax-workspace-selector]").forEach(function (node) {
    mount(node, {});
  });
}());
