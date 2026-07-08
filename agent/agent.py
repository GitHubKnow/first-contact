from armoriq_sdk import ArmorIQClient


class ArmorAgent:

    def __init__(self):

        self.client = ArmorIQClient()


    def build_plan(self, action):

        if action == "show_sales":

            return {
                "steps": [
                    {
                        "mcp": "sales-mcp",
                        "action": "fetch_sales",
                        "params": {}
                    }
                ]
            }


        elif action == "analyze_sales":

            return {
                "steps": [
                    {
                        "mcp": "sales-mcp",
                        "action": "analyze_sales",
                        "params": {}
                    }
                ]
            }


        else:

            raise ValueError(
                "Unknown action"
            )


    def execute(self, action):

        prompt = action


        # 1. Build execution plan

        plan = self.build_plan(action)


        print("\nPLAN:")
        print(plan)



        # 2. Capture plan with ArmorIQ

        plan_capture = self.client.capture_plan(
            llm="rule-based-planner",
            prompt=prompt,
            plan=plan
        )


        print("\nPLAN CAPTURE:")
        print(plan_capture)



        # 3. Generate intent token

        intent_token = self.client.get_intent_token(
            plan_capture
        )


        print("\nINTENT TOKEN:")
        print(intent_token.token_id)



        # 4. Execute through ArmorIQ MCP proxy

        step = plan["steps"][0]


        response = self.client.invoke(
            mcp=step["mcp"],
            action=step["action"],
            intent_token=intent_token,
            params=step["params"]
        )


        print("\nFINAL RESPONSE:")
        print(response)



        return response.result



# local testing only

if __name__ == "__main__":

    agent = ArmorAgent()

    result = agent.execute(
        "show_sales"
    )

    print(result)
