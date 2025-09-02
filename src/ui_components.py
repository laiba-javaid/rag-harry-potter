# src/ui_components.py - Harry Potter RAG UI Components
import gradio as gr
import random

class HarryPotterUI:
    def __init__(self):
        self.magical_quotes = [
            "⚡ 'It is our choices, Harry, that show what we truly are, far more than our abilities.' - Dumbledore",
            "🦌 'Happiness can be found, even in the darkest of times, if one only remembers to turn on the light.' - Dumbledore",
            "🪶 'Words are, in my not-so-humble opinion, our most inexhaustible source of magic.' - Dumbledore",
            "🔮 'It does not do to dwell on dreams and forget to live.' - Dumbledore",
            "⭐ 'We've all got both light and dark inside us. What matters is the part we choose to act on.' - Sirius Black"
        ]
        
        self.query_examples = {
            "🧙‍♂️ Character Analysis": [
                "How does Snape's character develop throughout the series?",
                "What are the key traits of Hermione Granger?",
                "Describe Harry's relationship with his father figures",
                "How does Draco Malfoy change over the books?"
            ],
            "📚 Plot & Events": [
                "Summarize the Triwizard Tournament from Goblet of Fire",
                "What happens during the Battle of Hogwarts?",
                "Explain the events of the Department of Mysteries",
                "Tell me about Harry's first Quidditch match"
            ],
            "🔍 Trivia & Details": [
                "What is Harry Potter's patronus and how did he learn it?",
                "What are the Deathly Hallows and their significance?",
                "How do you make a Polyjuice Potion?",
                "Who are the original members of the Order of the Phoenix?"
            ],
            "🏰 World Building": [
                "Describe the different houses at Hogwarts",
                "What is the history of the Marauder's Map?",
                "Explain the wizarding government structure",
                "Tell me about magical creatures in the series"
            ]
        }

    def create_custom_css(self):
        return """
        .gradio-container {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%) !important;
            font-family: 'Georgia', serif !important;
        }
        
        .main-header {
            background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            text-align: center !important;
            font-size: 2.5em !important;
            font-weight: bold !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
            margin: 20px 0 !important;
        }
        
        .magical-border {
            border: 2px solid #ffd700 !important;
            border-radius: 15px !important;
            background: rgba(255, 215, 0, 0.1) !important;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.3) !important;
            padding: 20px !important;
            margin: 15px 0 !important;
        }
        
        .spell-button {
            background: linear-gradient(45deg, #1a1a2e, #16213e) !important;
            border: 2px solid #ffd700 !important;
            color: #ffd700 !important;
            border-radius: 25px !important;
            padding: 10px 20px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        
        .spell-button:hover {
            background: linear-gradient(45deg, #ffd700, #ffed4e) !important;
            color: #1a1a2e !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5) !important;
            transform: translateY(-2px) !important;
        }
        
        .magical-text {
            color: #e6e6fa !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7) !important;
        }
        
        .golden-text {
            color: #ffd700 !important;
            font-weight: bold !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
        }
        
        .response-box {
            background: rgba(30, 30, 60, 0.8) !important;
            border: 1px solid #ffd700 !important;
            border-radius: 10px !important;
            padding: 15px !important;
            color: #e6e6fa !important;
            font-family: 'Georgia', serif !important;
            line-height: 1.6 !important;
            box-shadow: inset 0 0 10px rgba(255, 215, 0, 0.1) !important;
        }
        
        .example-card {
            background: rgba(255, 215, 0, 0.1) !important;
            border: 1px solid #ffd700 !important;
            border-radius: 10px !important;
            padding: 15px !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }
        
        .example-card:hover {
            background: rgba(255, 215, 0, 0.2) !important;
            transform: translateY(-5px) !important;
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3) !important;
        }
        
        .stats-container {
            display: flex !important;
            justify-content: space-around !important;
            background: rgba(255, 215, 0, 0.1) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            margin: 20px 0 !important;
        }
        
        .stat-item {
            text-align: center !important;
            color: #ffd700 !important;
        }
        """

    def create_advanced_interface(self, rag_pipeline_func):
        """Create the advanced interface - matches the method name in main.py"""
        return self.create_interface(rag_pipeline_func)

    def create_interface(self, rag_pipeline_func):
        css = self.create_custom_css()
        
        with gr.Blocks(css=css, title="⚡ Magical Harry Potter RAG Assistant") as interface:
            # Header Section
            gr.HTML("""
                <div class="main-header">
                    ⚡ MAGICAL HARRY POTTER RAG ASSISTANT 🏰
                </div>
                <div style="text-align: center; color: #ffd700; font-size: 1.2em; margin-bottom: 20px;">
                    <em>"Wit beyond measure is man's greatest treasure" - Ravenclaw House</em>
                </div>
            """)
            
            # Static magical quote (removed auto-refresh to fix compatibility)
            gr.HTML(f'''
                <div style="text-align: center; color: #e6e6fa; font-style: italic; margin: 15px 0; padding: 10px; background: rgba(255,215,0,0.1); border-radius: 10px;">
                    {random.choice(self.magical_quotes)}
                </div>
            ''')
            
            # Main interaction area
            with gr.Row():
                with gr.Column(scale=2):
                    with gr.Group():
                        gr.HTML('<div class="golden-text" style="font-size: 1.3em; margin-bottom: 10px;">🔮 Ask the Magical Oracle</div>')
                        
                        query_input = gr.Textbox(
                            label="",
                            placeholder="Ask me anything about the magical world of Harry Potter...",
                            lines=3,
                            elem_classes=["magical-border"]
                        )
                        
                        with gr.Row():
                            submit_btn = gr.Button("🪄 Cast Question Spell", variant="primary", elem_classes=["spell-button"])
                            clear_btn = gr.Button("🧹 Clear", variant="secondary", elem_classes=["spell-button"])
                            random_btn = gr.Button("🎲 Random Question", variant="secondary", elem_classes=["spell-button"])
                
                with gr.Column(scale=1):
                    gr.HTML('<div class="golden-text" style="font-size: 1.3em; margin-bottom: 10px;">📊 Knowledge Stats</div>')
                    stats_html = gr.HTML("""
                        <div class="stats-container">
                            <div class="stat-item">
                                <div style="font-size: 2em;">📚</div>
                                <div>7 Books</div>
                            </div>
                            <div class="stat-item">
                                <div style="font-size: 2em;">🧩</div>
                                <div>1000+ Chunks</div>
                            </div>
                            <div class="stat-item">
                                <div style="font-size: 2em;">⚡</div>
                                <div>AI Powered</div>
                            </div>
                        </div>
                    """)
            
            # Response area
            with gr.Group():
                gr.HTML('<div class="golden-text" style="font-size: 1.3em; margin-bottom: 10px;">📜 Magical Response</div>')
                response_output = gr.Textbox(
                    label="",
                    lines=12,
                    elem_classes=["response-box"],
                    interactive=False
                )
            
            # Example queries
            gr.HTML('<div class="golden-text" style="font-size: 1.5em; text-align: center; margin: 30px 0 20px 0;">🎭 Magical Query Categories</div>')
            
            with gr.Tabs():
                for category, examples in self.query_examples.items():
                    with gr.TabItem(category):
                        for example in examples:
                            btn = gr.Button(
                                example, 
                                elem_classes=["example-card"],
                                variant="secondary"
                            )
                            
                            # Connect each example button to input
                            btn.click(
                                fn=lambda x=example: x,
                                outputs=query_input
                            )
            
            # Advanced features section
            with gr.Accordion("🔧 Advanced Magical Features", open=False):
                with gr.Row():
                    with gr.Column():
                        gr.HTML("""
                            <div class="magical-border">
                                <h3 class="golden-text">🎯 Specialized Queries</h3>
                                <ul class="magical-text">
                                    <li><strong>Character Analysis:</strong> Deep dive into character development</li>
                                    <li><strong>Plot Summaries:</strong> Comprehensive event overviews</li>
                                    <li><strong>Trivia Questions:</strong> Specific details and facts</li>
                                    <li><strong>World Building:</strong> Magical world explanations</li>
                                </ul>
                            </div>
                        """)
                    
                    with gr.Column():
                        gr.HTML("""
                            <div class="magical-border">
                                <h3 class="golden-text">✨ AI Capabilities</h3>
                                <ul class="magical-text">
                                    <li><strong>Context Retrieval:</strong> Finds relevant book passages</li>
                                    <li><strong>Smart Summarization:</strong> Condenses complex information</li>
                                    <li><strong>Query Analysis:</strong> Optimizes retrieval strategy</li>
                                    <li><strong>Response Enhancement:</strong> Adds magical formatting</li>
                                </ul>
                            </div>
                        """)
            
            # Function to get random question
            def get_random_question():
                all_examples = [example for examples in self.query_examples.values() for example in examples]
                return random.choice(all_examples)
            
            # Enhanced RAG pipeline wrapper
            def enhanced_rag_pipeline(query):
                if not query.strip():
                    return "🪄 Please cast a question spell by typing your query above!"
                
                try:
                    response = rag_pipeline_func(query)
                    return response
                    
                except Exception as e:
                    return f"🚨 **Magical Error:** The spell backfired! {str(e)}"
            
            # Event handlers
            submit_btn.click(
                fn=enhanced_rag_pipeline,
                inputs=query_input,
                outputs=response_output
            )
            
            clear_btn.click(
                fn=lambda: ("", ""),
                outputs=[query_input, response_output]
            )
            
            random_btn.click(
                fn=get_random_question,
                outputs=query_input
            )
            
            # Footer
            gr.HTML("""
                <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(255,215,0,0.1); border-radius: 10px;">
                    <div class="golden-text" style="font-size: 1.2em; margin-bottom: 10px;">
                        🏰 Powered by Advanced RAG Magic 🏰
                    </div>
                    <div class="magical-text">
                        Combining the wisdom of all 7 Harry Potter books with cutting-edge AI<br>
                        <em>"After all this time?" "Always." - Severus Snape</em>
                    </div>
                </div>
            """)
        
        return interface