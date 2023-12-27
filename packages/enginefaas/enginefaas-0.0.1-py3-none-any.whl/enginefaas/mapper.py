NATIVE_FUNC_NS = "openfaas-fn"

def map_ns(component_ns, space_type, user_id=None):
    app_ns = NATIVE_FUNC_NS + "-" + component_ns.split(".")[0]

    if space_type == "prod":
        return app_ns
    if user_id is not None:
        user_ns = component_ns.split(".")[0] + "-" + user_id
        return user_ns 
    return app_ns + "-" + "dev"

def map_svc(component_ns, component_last_name):
    component_last_name = component_last_name.replace("_", "-", -1)
    component_ns = component_ns.replace("_", "-", -1)
    component_ns = component_ns.replace(".", "-", -1)
    svc_name = component_ns.lower() + "-" + component_last_name.lower()
    return svc_name
