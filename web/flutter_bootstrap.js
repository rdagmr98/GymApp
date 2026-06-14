{{flutter_js}}
{{flutter_build_config}}
_flutter.loader.load({
  config: {
    canvasKitBaseUrl: "canvaskit",
    wasmAllowList: {webkit: true}
  },
  serviceWorkerSettings: {
    serviceWorkerVersion: "{{flutter_service_worker_version}}"
  }
});
