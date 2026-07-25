def response_builder(message, state="failed", data=[]):
    if state.lower() == "success":
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    elif state.lower() == "failed":
        return {
            "success": False,
            "message": message
        }
