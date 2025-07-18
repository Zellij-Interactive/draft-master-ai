# LLM Concepts and Implementation in LoL Analysis App
## Comprehensive Guide to Language Model Integration

### 📋 Table of Contents
1. [LangChain-Style Prompt Engineering](#langchain-style-prompt-engineering)
2. [Prompt Templates and Chains](#prompt-templates-and-chains)
3. [Few-Shot Learning Implementation](#few-shot-learning-implementation)
4. [Chain-of-Thought Reasoning](#chain-of-thought-reasoning)
5. [Context Management](#context-management)
6. [Output Parsers](#output-parsers)
7. [Memory and State Management](#memory-and-state-management)

---

## 🔗 LangChain-Style Prompt Engineering

### Theory
LangChain introduces the concept of **prompt templates** and **chains** to create modular, reusable AI workflows. Instead of hardcoded prompts, we use templates that can be dynamically filled with context.

### Implementation in Our App

#### 1. System Prompt Templates
```python
# In utils/openai_utils.py - Current Implementation
SYSTEM_PROMPTS = {
    "team_analysis": """
    You are an expert League of Legends analyst specializing in team compositions.
    Analyze the given team composition and provide insights on:
    1. Team strengths and weaknesses
    2. Win conditions
    3. Overall team scaling
    4. Suggested playstyle
    5. Team fight potential
    
    Format your response as JSON with the following structure:
    {schema}
    """,
    
    "player_analysis": """
    You are an expert League of Legends analyst specializing in player performance.
    Based on the summoner name, champion selection, and match history provided, analyze:
    1. Player's strengths with the selected champion
    2. Areas for improvement
    3. Suggested itemization
    4. Key performance metrics to focus on
    
    Format your response as JSON with the following structure:
    {schema}
    """
}
```

#### 2. LangChain-Style Template System
```python
# Enhanced implementation with LangChain concepts
class PromptTemplate:
    def __init__(self, template: str, input_variables: list):
        self.template = template
        self.input_variables = input_variables
    
    def format(self, **kwargs):
        """Format template with provided variables"""
        return self.template.format(**kwargs)

# Team Analysis Template
TEAM_ANALYSIS_TEMPLATE = PromptTemplate(
    template="""
    You are an expert League of Legends analyst with {experience_years} years of experience.
    
    Current Meta Context:
    - Patch Version: {patch_version}
    - Meta Trends: {meta_trends}
    - Regional Preferences: {region}
    
    Team Composition to Analyze:
    Blue Team: {blue_team}
    Red Team: {red_team}
    Analysis Perspective: {perspective}
    
    {few_shot_examples}
    
    Provide detailed analysis following the examples above.
    Focus on {analysis_focus} for this {player_rank} level analysis.
    
    Response Format: {response_schema}
    """,
    input_variables=[
        "experience_years", "patch_version", "meta_trends", "region",
        "blue_team", "red_team", "perspective", "few_shot_examples",
        "analysis_focus", "player_rank", "response_schema"
    ]
)
```

---

## 🔗 Prompt Templates and Chains

### Theory
**Chains** in LangChain allow you to connect multiple LLM calls or processing steps. This enables complex workflows where the output of one step becomes the input of another.

### Implementation: Analysis Chain

```python
class AnalysisChain:
    def __init__(self, openai_client, gemini_client):
        self.openai_client = openai_client
        self.gemini_client = gemini_client
    
    def run_complete_analysis(self, user_input):
        """
        Multi-step analysis chain:
        1. Get current meta context (Gemini)
        2. Analyze team composition (OpenAI)
        3. Generate matchup insights (OpenAI)
        4. Combine and enhance results
        """
        
        # Step 1: Meta Context Chain
        meta_context = self._get_meta_context()
        
        # Step 2: Team Analysis Chain
        team_analysis = self._analyze_team_composition(
            user_input, meta_context
        )
        
        # Step 3: Matchup Analysis Chain
        matchup_analysis = self._analyze_matchups(
            user_input, meta_context, team_analysis
        )
        
        # Step 4: Result Enhancement Chain
        enhanced_results = self._enhance_results(
            team_analysis, matchup_analysis, meta_context
        )
        
        return enhanced_results
    
    def _get_meta_context(self):
        """Chain Step 1: Get current meta context"""
        meta_prompt = PromptTemplate(
            template="""
            Analyze the current League of Legends meta:
            
            Tasks:
            1. Identify trending champions by role
            2. Assess current patch impact
            3. Predict meta shifts
            
            Format: {meta_schema}
            """,
            input_variables=["meta_schema"]
        )
        
        formatted_prompt = meta_prompt.format(
            meta_schema=META_RESPONSE_SCHEMA
        )
        
        return self.gemini_client.generate_content(formatted_prompt)
    
    def _analyze_team_composition(self, user_input, meta_context):
        """Chain Step 2: Analyze team composition with meta context"""
        team_prompt = TEAM_ANALYSIS_TEMPLATE.format(
            experience_years="10+",
            patch_version=meta_context.get("patch_version", "14.1"),
            meta_trends=meta_context.get("trends", []),
            region=user_input.get("region", "Global"),
            blue_team=user_input["blue_team"],
            red_team=user_input["red_team"],
            perspective=user_input["perspective"],
            few_shot_examples=TEAM_ANALYSIS_EXAMPLES,
            analysis_focus="strategic depth",
            player_rank=user_input.get("rank", "Gold"),
            response_schema=TEAM_RESPONSE_SCHEMA
        )
        
        return self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": team_prompt},
                {"role": "user", "content": "Analyze this team composition."}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
```

---

## 🎯 Few-Shot Learning Implementation

### Theory
**Few-shot learning** provides the LLM with examples of desired input-output pairs to improve response quality and consistency. This is crucial for domain-specific applications like LoL analysis.

### Current Status in App
**Currently NOT implemented** - the app uses zero-shot prompting. Here's how to add it:

```python
# Few-shot examples for team analysis
TEAM_ANALYSIS_EXAMPLES = """
Here are examples of excellent team composition analysis:

Example 1:
Input: Blue Team: Malphite, Graves, Yasuo, Jinx, Leona
Analysis: {
    "summary": "This is a teamfight-oriented composition with strong engage potential and excellent scaling. The team excels at forcing 5v5 teamfights around objectives with Malphite and Leona providing multiple engage tools while protecting Jinx for late-game carry potential.",
    "strengths": [
        "Excellent teamfight potential with multiple engage tools",
        "Strong frontline with Malphite and Leona",
        "Yasuo synergy with Malphite ultimate for devastating combos",
        "Jinx hypercarry potential in late game teamfights"
    ],
    "weaknesses": [
        "Vulnerable to poke compositions before teamfights",
        "Limited mobility and kiting potential",
        "Reliant on landing key engage abilities",
        "Weak early game laning phase"
    ],
    "win_conditions": [
        "Force teamfights around Dragon and Baron",
        "Protect Jinx positioning in teamfights",
        "Land Malphite + Yasuo combo for fight initiation",
        "Scale safely to 3+ items on carries"
    ],
    "scaling": "7/10 - Strong late game scaling",
    "playstyle": "Teamfight-focused with emphasis on objective control",
    "teamfight": "Excellent teamfight potential with multiple engage tools and AoE damage"
}

Example 2:
Input: Blue Team: Fiora, Nidalee, LeBlanc, Lucian, Thresh
Analysis: {
    "summary": "This is an early-game focused composition with strong skirmishing potential and pick potential. The team excels at creating early leads through superior mobility and burst damage.",
    "strengths": [
        "Strong early game pressure in all lanes",
        "Excellent mobility and pick potential",
        "High burst damage for quick eliminations",
        "Good skirmishing around objectives"
    ],
    "weaknesses": [
        "Falls off significantly in late game",
        "Lacks sustained damage in teamfights",
        "Vulnerable to hard engage compositions",
        "Requires early leads to remain relevant"
    ],
    "win_conditions": [
        "Snowball early game advantages",
        "Control vision for picks with Thresh and Nidalee",
        "End game before 30 minutes",
        "Focus on split-pushing with Fiora"
    ],
    "scaling": "3/10 - Early game focused",
    "playstyle": "Aggressive early game with pick-focused mid game",
    "teamfight": "Weak teamfight potential, focus on picks and skirmishes"
}

Now analyze the following team composition following these examples:
"""

# Implementation in the analysis function
def get_analysis_with_few_shot(analysis_type, data):
    """Enhanced analysis with few-shot learning"""
    
    # Get appropriate examples
    examples = FEW_SHOT_EXAMPLES.get(analysis_type, "")
    
    # Create enhanced prompt
    system_prompt = f"""
    {SYSTEM_PROMPTS[analysis_type]}
    
    {examples}
    
    Follow the format and depth shown in the examples above.
    """
    
    # Continue with API call...
```

### Benefits of Few-Shot Learning in Our App
1. **Consistency**: Ensures similar structure across all analyses
2. **Quality**: Provides examples of high-quality analysis depth
3. **Domain Knowledge**: Shows LoL-specific terminology and concepts
4. **Format Adherence**: Demonstrates proper JSON structure

---

## 🧠 Chain-of-Thought Reasoning

### Theory
**Chain-of-Thought (CoT)** prompting guides the LLM through step-by-step reasoning, improving accuracy for complex analytical tasks.

### Implementation in Our App

```python
# Current basic implementation
def get_team_analysis(data):
    user_prompt = f"""
    Blue Team: {', '.join(data['blue'])}
    Red Team: {', '.join(data['red'])}
    Team to analyze: {data['side']}
    
    Provide detailed team composition analysis.
    """

# Enhanced Chain-of-Thought implementation
CHAIN_OF_THOUGHT_TEMPLATE = """
Analyze this team composition step by step:

Step 1: Individual Champion Analysis
- Analyze each champion's strengths, weaknesses, and role
- Consider their current meta standing and recent changes
- Assess their synergy potential with teammates

Step 2: Team Synergy Evaluation
- Identify positive synergies between champions
- Note potential anti-synergies or conflicts
- Evaluate overall team cohesion

Step 3: Win Condition Assessment
- Determine the team's primary win conditions
- Assess scaling patterns and power spikes
- Identify key teamfight scenarios

Step 4: Strategic Recommendations
- Provide specific gameplay recommendations
- Suggest itemization priorities
- Recommend macro strategies

Team Composition: {team_comp}
Current Meta Context: {meta_context}

Please follow each step and provide detailed reasoning for your conclusions.

Final Analysis Format: {response_schema}
"""

def get_cot_analysis(team_data, meta_context):
    """Get analysis using Chain-of-Thought reasoning"""
    
    cot_prompt = CHAIN_OF_THOUGHT_TEMPLATE.format(
        team_comp=format_team_composition(team_data),
        meta_context=meta_context,
        response_schema=TEAM_RESPONSE_SCHEMA
    )
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": cot_prompt},
            {"role": "user", "content": "Analyze this team composition step by step."}
        ],
        temperature=0.7
    )
    
    return response
```

### Benefits of CoT in LoL Analysis
1. **Better Reasoning**: Step-by-step analysis improves accuracy
2. **Transparency**: Users can see the reasoning process
3. **Comprehensive Coverage**: Ensures all aspects are considered
4. **Educational Value**: Teaches users analytical thinking

---

## 🧩 Context Management

### Theory
**Context management** involves efficiently handling the information flow between different parts of the conversation and maintaining relevant context across multiple interactions.

### Implementation in Our App

```python
# Current context management in session_state.py
def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "current_patch_analysis" not in st.session_state:
        st.session_state.current_patch_analysis = {}

# Enhanced context management
class ContextManager:
    def __init__(self):
        self.context_layers = {
            "session": {},      # User session data
            "meta": {},         # Current meta information
            "analysis": {},     # Previous analysis results
            "preferences": {}   # User preferences
        }
    
    def build_analysis_context(self, user_input):
        """Build comprehensive context for analysis"""
        context = {
            # User context
            "summoner_name": user_input.get("summoner_name"),
            "region": user_input.get("region"),
            "rank": self.get_user_rank(),
            
            # Meta context
            "patch_version": self.get_current_patch(),
            "meta_trends": self.get_meta_trends(),
            "champion_tiers": self.get_champion_tiers(),
            
            # Historical context
            "previous_analyses": self.get_recent_analyses(),
            "user_preferences": self.get_user_preferences(),
            
            # Game context
            "team_composition": user_input["team_comp"],
            "analysis_perspective": user_input["perspective"]
        }
        
        return context
    
    def update_context(self, analysis_results):
        """Update context with new analysis results"""
        self.context_layers["analysis"]["last_analysis"] = {
            "timestamp": datetime.now(),
            "results": analysis_results,
            "quality_score": self.calculate_quality_score(analysis_results)
        }
    
    def get_relevant_context(self, analysis_type):
        """Get context relevant to specific analysis type"""
        base_context = self.context_layers["session"]
        
        if analysis_type == "team_analysis":
            return {
                **base_context,
                "meta_context": self.context_layers["meta"],
                "champion_synergies": self.get_champion_synergies()
            }
        elif analysis_type == "player_analysis":
            return {
                **base_context,
                "player_history": self.get_player_history(),
                "champion_mastery": self.get_champion_mastery()
            }
        
        return base_context
```

---

## 🔍 Output Parsers

### Theory
**Output parsers** ensure that LLM responses are properly formatted and validated before being used by the application.

### Implementation in Our App

```python
# Current basic JSON parsing in openai_utils.py
result = json.loads(response.choices[0].message.content)

# Enhanced output parser implementation
class AnalysisOutputParser:
    def __init__(self):
        self.schemas = {
            "team_analysis": TEAM_ANALYSIS_SCHEMA,
            "player_analysis": PLAYER_ANALYSIS_SCHEMA,
            "matchup_analysis": MATCHUP_ANALYSIS_SCHEMA
        }
    
    def parse(self, raw_output: str, analysis_type: str):
        """Parse and validate LLM output"""
        try:
            # Clean the output
            cleaned_output = self._clean_json_output(raw_output)
            
            # Parse JSON
            parsed_data = json.loads(cleaned_output)
            
            # Validate against schema
            validation_errors = self._validate_schema(
                parsed_data, 
                self.schemas[analysis_type]
            )
            
            if validation_errors:
                return self._handle_validation_errors(
                    parsed_data, validation_errors, analysis_type
                )
            
            # Enhance with metadata
            enhanced_data = self._enhance_output(parsed_data, analysis_type)
            
            return enhanced_data
            
        except json.JSONDecodeError as e:
            return self._handle_json_error(raw_output, analysis_type)
        except Exception as e:
            return self._handle_general_error(e, analysis_type)
    
    def _clean_json_output(self, raw_output: str) -> str:
        """Clean common JSON formatting issues"""
        # Remove markdown code blocks
        if raw_output.startswith('```json'):
            raw_output = raw_output[7:]
        if raw_output.endswith('```'):
            raw_output = raw_output[:-3]
        
        # Remove trailing commas
        import re
        raw_output = re.sub(r',(\s*[}\]])', r'\1', raw_output)
        
        return raw_output.strip()
    
    def _validate_schema(self, data: dict, schema: dict) -> list:
        """Validate data against expected schema"""
        errors = []
        
        # Check required fields
        for field in schema.get("required", []):
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Check field types
        for field, expected_type in schema.get("types", {}).items():
            if field in data and not isinstance(data[field], expected_type):
                errors.append(f"Field '{field}' should be {expected_type.__name__}")
        
        # Check minimum lengths for arrays
        for field, min_length in schema.get("min_lengths", {}).items():
            if field in data and isinstance(data[field], list):
                if len(data[field]) < min_length:
                    errors.append(f"Field '{field}' needs at least {min_length} items")
        
        return errors
    
    def _enhance_output(self, data: dict, analysis_type: str) -> dict:
        """Enhance output with additional metadata"""
        enhanced = data.copy()
        enhanced["_metadata"] = {
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat(),
            "confidence_score": self._calculate_confidence(data),
            "quality_indicators": self._assess_quality(data)
        }
        return enhanced

# Schema definitions
TEAM_ANALYSIS_SCHEMA = {
    "required": ["summary", "strengths", "weaknesses", "win_conditions"],
    "types": {
        "summary": str,
        "strengths": list,
        "weaknesses": list,
        "win_conditions": list,
        "scaling": str,
        "playstyle": str,
        "teamfight": str
    },
    "min_lengths": {
        "strengths": 2,
        "weaknesses": 2,
        "win_conditions": 2
    }
}
```

---

## 💾 Memory and State Management

### Theory
**Memory systems** in LLM applications maintain context across multiple interactions, enabling more coherent and personalized experiences.

### Implementation in Our App

```python
# Current session state management
# In utils/session_state.py - basic implementation

# Enhanced memory system
class AnalysisMemory:
    def __init__(self):
        self.short_term_memory = {}  # Current session
        self.long_term_memory = {}   # Persistent across sessions
        self.working_memory = {}     # Active analysis context
    
    def store_analysis(self, analysis_id: str, analysis_data: dict):
        """Store analysis in memory systems"""
        
        # Short-term memory (current session)
        self.short_term_memory[analysis_id] = {
            "data": analysis_data,
            "timestamp": datetime.now(),
            "access_count": 0
        }
        
        # Working memory (active context)
        self.working_memory["last_analysis"] = analysis_data
        self.working_memory["analysis_history"] = self._get_recent_analyses(5)
        
        # Long-term memory (persistent patterns)
        self._update_user_patterns(analysis_data)
    
    def get_relevant_memory(self, query_context: dict) -> dict:
        """Retrieve relevant memory for current query"""
        relevant_memory = {}
        
        # Get similar past analyses
        similar_analyses = self._find_similar_analyses(query_context)
        if similar_analyses:
            relevant_memory["similar_analyses"] = similar_analyses
        
        # Get user patterns
        user_patterns = self._get_user_patterns(query_context)
        if user_patterns:
            relevant_memory["user_patterns"] = user_patterns
        
        # Get contextual information
        contextual_info = self._get_contextual_info(query_context)
        if contextual_info:
            relevant_memory["context"] = contextual_info
        
        return relevant_memory
    
    def _find_similar_analyses(self, query_context: dict) -> list:
        """Find analyses similar to current query"""
        similar = []
        
        for analysis_id, analysis in self.short_term_memory.items():
            similarity_score = self._calculate_similarity(
                query_context, 
                analysis["data"]
            )
            
            if similarity_score > 0.7:  # Threshold for similarity
                similar.append({
                    "analysis_id": analysis_id,
                    "similarity": similarity_score,
                    "data": analysis["data"]
                })
        
        return sorted(similar, key=lambda x: x["similarity"], reverse=True)
    
    def _update_user_patterns(self, analysis_data: dict):
        """Update long-term user patterns"""
        user_id = self._get_user_id()
        
        if user_id not in self.long_term_memory:
            self.long_term_memory[user_id] = {
                "preferred_champions": {},
                "analysis_patterns": {},
                "feedback_history": []
            }
        
        # Update champion preferences
        team_comp = analysis_data.get("team_composition", {})
        for team, champions in team_comp.items():
            for champion in champions:
                if champion:
                    self._increment_champion_preference(user_id, champion)
        
        # Update analysis patterns
        self._update_analysis_patterns(user_id, analysis_data)

# Integration with main analysis flow
class EnhancedAnalysisEngine:
    def __init__(self):
        self.memory = AnalysisMemory()
        self.context_manager = ContextManager()
        self.output_parser = AnalysisOutputParser()
    
    def analyze_with_memory(self, user_input: dict) -> dict:
        """Perform analysis with memory integration"""
        
        # Build context with memory
        base_context = self.context_manager.build_analysis_context(user_input)
        memory_context = self.memory.get_relevant_memory(base_context)
        
        # Combine contexts
        full_context = {**base_context, **memory_context}
        
        # Generate analysis with enhanced context
        raw_analysis = self._generate_analysis(user_input, full_context)
        
        # Parse and validate output
        parsed_analysis = self.output_parser.parse(
            raw_analysis, 
            user_input["analysis_type"]
        )
        
        # Store in memory
        analysis_id = self._generate_analysis_id(user_input)
        self.memory.store_analysis(analysis_id, parsed_analysis)
        
        # Update context
        self.context_manager.update_context(parsed_analysis)
        
        return parsed_analysis
```

---

## 🔄 Integration Summary

### How These Concepts Work Together in Our App

1. **Prompt Templates** → Create reusable, dynamic prompts
2. **Few-Shot Learning** → Improve response quality with examples
3. **Chain-of-Thought** → Guide step-by-step reasoning
4. **Context Management** → Maintain relevant information flow
5. **Output Parsers** → Ensure reliable, validated responses
6. **Memory Systems** → Enable personalized, coherent experiences

### Current Implementation Status

| Concept | Status | Location |
|---------|--------|----------|
| **Basic Prompts** | ✅ Implemented | `utils/openai_utils.py` |
| **System Prompts** | ✅ Implemented | `SYSTEM_PROMPTS` dict |
| **JSON Parsing** | ✅ Implemented | `get_analysis()` function |
| **Session State** | ✅ Implemented | `utils/session_state.py` |
| **Few-Shot Learning** | ❌ Not implemented | Need to add examples |
| **Chain-of-Thought** | ❌ Not implemented | Need CoT templates |
| **Advanced Context** | ⚠️ Partial | Basic session state only |
| **Output Validation** | ⚠️ Partial | Basic JSON parsing only |
| **Memory Systems** | ❌ Not implemented | Need persistent memory |

### Next Steps for Enhancement

1. **Add Few-Shot Examples** → Improve response consistency
2. **Implement CoT Prompting** → Better analytical reasoning
3. **Enhanced Context Management** → More intelligent context handling
4. **Robust Output Parsing** → Better error handling and validation
5. **Memory Integration** → Personalized user experiences

This comprehensive implementation would transform the app from basic LLM integration to a sophisticated, LangChain-style AI system with advanced prompt engineering and context management.