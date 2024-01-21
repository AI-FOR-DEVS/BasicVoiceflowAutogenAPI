from flask import Flask, jsonify, request
import autogen

app = Flask(__name__)

@app.route('/run')
def spare_parts():
    query = request.args.get('query')

    config_list = autogen.config_list_from_json('OAI_CONFIG_LIST')

    assistant = autogen.AssistantAgent(
        "assistant", llm_config={"config_list": config_list}
    )

    user_proxy = autogen.UserProxyAgent(
        "user_proxy", 
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "") and x.get(
            "content", "").rstrip().endswith("TERMINATE")
    )

    user_proxy.initiate_chat(
        assistant, 
        message=f"""
          Return the availability and price of the requested spare part 
          and send 'TERMINATE'. You can make things up, don't run any code.

          Request: '{query}'

          Output Format: 'Availability: In stock \n Price:'
        """
    )

    answer = user_proxy.chat_messages[assistant][1]['content']

    return jsonify({"spare_parts": answer})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)