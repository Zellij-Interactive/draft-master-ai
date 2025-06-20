# Language Model Theory and Implementation
## Deep Dive into AI Integration

### 📋 Table of Contents
1. [Language Model Fundamentals](#language-model-fundamentals)
2. [Multi-Model Architecture](#multi-model-architecture)
3. [Prompt Engineering](#prompt-engineering)
4. [Context Management](#context-management)
5. [Response Processing](#response-processing)
6. [Performance Optimization](#performance-optimization)
7. [Error Handling](#error-handling)
8. [Advanced Techniques](#advanced-techniques)

---

## 🧠 Language Model Fundamentals

### Understanding Large Language Models (LLMs)

Large Language Models are neural networks trained on vast amounts of text data to understand and generate human-like text. In our League of Legends analysis application, we leverage multiple LLMs for different specialized tasks.

#### Key Concepts

1. **Transformer Architecture**
   - Self-attention mechanisms for understanding context
   - Parallel processing for efficiency
   - Positional encoding for sequence understanding

2. **Training Process**
   - Pre-training on diverse text corpora
   - Fine-tuning for specific tasks
   - Reinforcement Learning from Human Feedback (RLHF)

3. **Emergent Capabilities**
   - Few-shot learning
   - Chain-of-thought reasoning
   - Task generalization

### Model Selection Rationale

#### OpenAI GPT-3.5 Turbo
**Strengths:**
- Excellent reasoning capabilities
- Strong performance on analytical tasks
- Reliable JSON output formatting
- Good balance of cost and performance

**Use Cases in Our App:**
- Team composition analysis
- Strategic recommendations
- Player performance evaluation

```python
# GPT-3.5 Turbo Configuration
model_config = {
    "model": "gpt-3.5-turbo-1106",
    "temperature": 0.7,  # Balanced creativity/consistency
    "max_tokens": 2000,  # Sufficient for detailed analysis
    "response_format": {"type": "json_object"}  # Structured output
}
```

#### Google Gemini 1.5 Flash
**Strengths:**
- Fast inference speed
- Large context window (1M+ tokens)
- Cost-effective for frequent queries
- Strong multimodal capabilities

**Use Cases in Our App:**
- Real-time patch analysis
- Meta trend prediction
- Large context processing

```python
# Gemini Configuration
gemini_config = {
    "model": "gemini-1.5-flash",
    "generation_config": {
        "temperature": 0.8,
        "top_p": 0.95,
        "max_output_tokens": 1500
    }
}
```

---

## 🏗️ Multi-Model Architecture

### Specialized Model Assignment

Our application uses a **divide-and-conquer** approach, assigning different models to tasks they excel at:

```python
class AIOrchestrator:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.gemini_client = GeminiClient()
        
    def route_request(self, task_type, data):
        """Route requests to appropriate model based on task"""
        routing_map = {
            "team_analysis": self.openai_client,
            "player_analysis": self.openai_client,
            "matchup_insights": self.openai_client,
            "patch_analysis": self.gemini_client,
            "meta_prediction": self.gemini_client,
            "video_analysis": self.gemini_client
        }
        
        client = routing_map.get(task_type, self.openai_client)
        return client.generate_analysis(task_type, data)
```

### Model Comparison Matrix

| Feature | GPT-3.5 Turbo | Gemini 1.5 Flash |
|---------|---------------|-------------------|
| **Reasoning** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Context Window** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cost** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **JSON Formatting** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Gaming Knowledge** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎯 Prompt Engineering

### Prompt Engineering Principles

#### 1. Role-Based Prompting
Establish clear expertise and context:

```python
EXPERT_ROLES = {
    "team_analyst": """
    You are a professional League of Legends analyst with 10+ years of experience 
    in competitive gaming. You specialize in team composition analysis and have 
    worked with LCS, LEC, and LCK teams. Your analysis is used by professional 
    coaches and players to gain competitive advantages.
    """,
    
    "meta_expert": """
    You are a League of Legends meta expert who tracks patch changes, champion 
    statistics, and professional play trends. You have deep knowledge of how 
    balance changes affect the competitive landscape and can predict meta shifts 
    before they become mainstream.
    """
}
```

#### 2. Structured Output Formatting
Ensure consistent, parseable responses:

```python
def create_structured_prompt(role, task, data, output_schema):
    """Create a structured prompt with clear output format"""
    return f"""
    {role}
    
    Task: {task}
    
    Data: {json.dumps(data, indent=2)}
    
    Please analyze the provided data and respond with a JSON object following 
    this exact schema:
    
    {json.dumps(output_schema, indent=2)}
    
    Important:
    - Provide specific, actionable insights
    - Base recommendations on current meta knowledge
    - Include confidence levels where appropriate
    - Ensure all array fields contain at least one item
    """
```

#### 3. Context Injection
Provide relevant contextual information:

```python
def inject_context(base_prompt, context_data):
    """Inject relevant context into prompts"""
    context_sections = []
    
    # Current patch context
    if 'patch_version' in context_data:
        context_sections.append(f"""
        Current Patch: {context_data['patch_version']}
        Key Changes: {', '.join(context_data.get('patch_changes', []))}
        """)
    
    # Regional meta context
    if 'region' in context_data:
        context_sections.append(f"""
        Region: {context_data['region']}
        Regional Meta Preferences: {context_data.get('regional_meta', 'Standard')}
        """)
    
    # Player skill context
    if 'player_rank' in context_data:
        context_sections.append(f"""
        Player Rank: {context_data['player_rank']}
        Skill Level Considerations: {get_skill_considerations(context_data['player_rank'])}
        """)
    
    context_string = "\n".join(context_sections)
    return f"{base_prompt}\n\nContext:\n{context_string}"
```

### Advanced Prompt Techniques

#### Chain-of-Thought Reasoning
Guide the model through step-by-step analysis:

```python
CHAIN_OF_THOUGHT_TEMPLATE = """
Analyze this team composition step by step:

Step 1: Individual Champion Analysis
- Analyze each champion's strengths, weaknesses, and role
- Consider their current meta standing

Step 2: Synergy Evaluation
- Identify positive synergies between champions
- Note potential anti-synergies or conflicts

Step 3: Team Identity Assessment
- Determine the team's primary win conditions
- Assess scaling patterns and power spikes

Step 4: Strategic Recommendations
- Provide specific gameplay recommendations
- Suggest itemization and macro strategies

Team Composition: {team_comp}
Current Meta Context: {meta_context}

Please follow each step and provide detailed reasoning for your conclusions.
"""
```

#### Few-Shot Learning Examples
Provide examples to guide response format:

```python
FEW_SHOT_EXAMPLES = """
Example Analysis 1:
Input: Team: Malphite, Graves, Yasuo, Jinx, Leona
Output: {
    "summary": "This is a teamfight-oriented composition with strong engage potential...",
    "strengths": ["Excellent teamfight potential", "Strong engage tools", "Good scaling"],
    "win_conditions": ["Force teamfights around objectives", "Protect Jinx in late game"]
}

Example Analysis 2:
Input: Team: Fiora, Nidalee, LeBlanc, Lucian, Thresh
Output: {
    "summary": "This is an early-game focused composition with strong skirmishing...",
    "strengths": ["Strong early game", "High mobility", "Pick potential"],
    "win_conditions": ["Snowball early leads", "Control vision for picks"]
}

Now analyze the following team:
Input: Team: {actual_team}
"""
```

---

## 🧩 Context Management

### Context Window Optimization

#### Token Management
```python
class TokenManager:
    def __init__(self, model_name):
        self.model_limits = {
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-1106": 16385,
            "gemini-1.5-flash": 1048576
        }
        self.max_tokens = self.model_limits.get(model_name, 4096)
    
    def estimate_tokens(self, text):
        """Rough token estimation (1 token ≈ 4 characters)"""
        return len(text) // 4
    
    def truncate_context(self, prompt, max_context_tokens):
        """Truncate context to fit within token limits"""
        estimated_tokens = self.estimate_tokens(prompt)
        
        if estimated_tokens <= max_context_tokens:
            return prompt
        
        # Truncate from the middle, keeping beginning and end
        truncation_ratio = max_context_tokens / estimated_tokens
        keep_length = int(len(prompt) * truncation_ratio)
        
        start_keep = keep_length // 2
        end_keep = keep_length - start_keep
        
        return prompt[:start_keep] + "\n[...context truncated...]\n" + prompt[-end_keep:]
```

#### Context Prioritization
```python
def prioritize_context(context_data, max_tokens):
    """Prioritize context elements by importance"""
    priority_order = [
        "current_patch",      # Highest priority
        "team_composition",
        "player_stats",
        "meta_trends",
        "historical_data"     # Lowest priority
    ]
    
    final_context = {}
    used_tokens = 0
    
    for priority_key in priority_order:
        if priority_key in context_data:
            key_tokens = estimate_tokens(str(context_data[priority_key]))
            
            if used_tokens + key_tokens <= max_tokens:
                final_context[priority_key] = context_data[priority_key]
                used_tokens += key_tokens
            else:
                # Truncate this context element if possible
                remaining_tokens = max_tokens - used_tokens
                if remaining_tokens > 100:  # Minimum useful context
                    truncated_data = truncate_data(
                        context_data[priority_key], 
                        remaining_tokens
                    )
                    final_context[priority_key] = truncated_data
                break
    
    return final_context
```

### Dynamic Context Adaptation

#### Adaptive Context Selection
```python
class AdaptiveContextManager:
    def __init__(self):
        self.context_effectiveness = {}
    
    def select_context(self, task_type, available_context):
        """Select most effective context for specific tasks"""
        task_context_map = {
            "team_analysis": [
                "champion_synergies",
                "current_meta",
                "patch_changes",
                "team_compositions"
            ],
            "player_analysis": [
                "player_stats",
                "champion_mastery",
                "recent_matches",
                "rank_data"
            ],
            "matchup_analysis": [
                "champion_matchups",
                "lane_statistics",
                "counter_picks",
                "professional_play"
            ]
        }
        
        relevant_keys = task_context_map.get(task_type, [])
        selected_context = {}
        
        for key in relevant_keys:
            if key in available_context:
                selected_context[key] = available_context[key]
        
        return selected_context
    
    def update_effectiveness(self, context_keys, analysis_quality):
        """Update context effectiveness based on analysis quality"""
        for key in context_keys:
            if key not in self.context_effectiveness:
                self.context_effectiveness[key] = []
            
            self.context_effectiveness[key].append(analysis_quality)
            
            # Keep only recent effectiveness scores
            if len(self.context_effectiveness[key]) > 10:
                self.context_effectiveness[key] = self.context_effectiveness[key][-10:]
```

---

## 🔄 Response Processing

### JSON Response Parsing

#### Robust JSON Extraction
```python
import re
import json

class ResponseProcessor:
    def __init__(self):
        self.json_patterns = [
            r'```json\s*(.*?)\s*```',  # Markdown code blocks
            r'```\s*(.*?)\s*```',      # Generic code blocks
            r'\{.*\}',                 # Direct JSON objects
        ]
    
    def extract_json(self, response_text):
        """Extract JSON from various response formats"""
        # Clean the response
        cleaned_text = response_text.strip()
        
        # Try direct JSON parsing first
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass
        
        # Try pattern matching
        for pattern in self.json_patterns:
            matches = re.findall(pattern, cleaned_text, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                try:
                    return json.loads(match.strip())
                except json.JSONDecodeError:
                    continue
        
        # If all else fails, try to fix common JSON issues
        return self.fix_and_parse_json(cleaned_text)
    
    def fix_and_parse_json(self, text):
        """Attempt to fix common JSON formatting issues"""
        fixes = [
            # Remove trailing commas
            (r',(\s*[}\]])', r'\1'),
            # Fix single quotes to double quotes
            (r"'([^']*)':", r'"\1":'),
            # Fix unquoted keys
            (r'(\w+):', r'"\1":'),
        ]
        
        fixed_text = text
        for pattern, replacement in fixes:
            fixed_text = re.sub(pattern, replacement, fixed_text)
        
        try:
            return json.loads(fixed_text)
        except json.JSONDecodeError:
            return None
```

#### Response Validation
```python
def validate_response_structure(response, expected_schema):
    """Validate response against expected schema"""
    validation_errors = []
    
    # Check required fields
    for field in expected_schema.get('required', []):
        if field not in response:
            validation_errors.append(f"Missing required field: {field}")
    
    # Check field types
    for field, expected_type in expected_schema.get('types', {}).items():
        if field in response:
            actual_type = type(response[field])
            if not isinstance(response[field], expected_type):
                validation_errors.append(
                    f"Field '{field}' expected {expected_type.__name__}, "
                    f"got {actual_type.__name__}"
                )
    
    # Check array lengths
    for field, min_length in expected_schema.get('min_lengths', {}).items():
        if field in response and isinstance(response[field], list):
            if len(response[field]) < min_length:
                validation_errors.append(
                    f"Field '{field}' must have at least {min_length} items"
                )
    
    return validation_errors

# Schema definitions
TEAM_ANALYSIS_SCHEMA = {
    'required': ['summary', 'strengths', 'weaknesses', 'win_conditions'],
    'types': {
        'summary': str,
        'strengths': list,
        'weaknesses': list,
        'win_conditions': list,
        'scaling': str
    },
    'min_lengths': {
        'strengths': 2,
        'weaknesses': 2,
        'win_conditions': 2
    }
}
```

### Response Enhancement

#### Post-Processing Pipeline
```python
class ResponseEnhancer:
    def __init__(self):
        self.enhancement_pipeline = [
            self.add_confidence_scores,
            self.enrich_with_metadata,
            self.add_contextual_links,
            self.format_for_display
        ]
    
    def enhance_response(self, raw_response, context):
        """Run response through enhancement pipeline"""
        enhanced_response = raw_response.copy()
        
        for enhancement_func in self.enhancement_pipeline:
            try:
                enhanced_response = enhancement_func(enhanced_response, context)
            except Exception as e:
                st.warning(f"Enhancement step failed: {e}")
        
        return enhanced_response
    
    def add_confidence_scores(self, response, context):
        """Add confidence scores to analysis points"""
        # Simple heuristic-based confidence scoring
        confidence_factors = {
            'meta_alignment': 0.8,  # High confidence in meta analysis
            'statistical_backing': 0.9,  # High confidence with stats
            'professional_play': 0.7,  # Medium confidence from pro play
            'theoretical': 0.6  # Lower confidence for theoretical analysis
        }
        
        for key, items in response.items():
            if isinstance(items, list):
                enhanced_items = []
                for item in items:
                    # Determine confidence based on content
                    confidence = self.calculate_confidence(item, context)
                    enhanced_items.append({
                        'content': item,
                        'confidence': confidence
                    })
                response[f"{key}_enhanced"] = enhanced_items
        
        return response
    
    def calculate_confidence(self, content, context):
        """Calculate confidence score for analysis content"""
        base_confidence = 0.7
        
        # Boost confidence for meta-aligned suggestions
        if any(meta_term in content.lower() for meta_term in ['meta', 'current', 'patch']):
            base_confidence += 0.1
        
        # Boost confidence for specific champion mentions
        if any(champ in content for champ in context.get('champions', [])):
            base_confidence += 0.1
        
        # Cap at 1.0
        return min(base_confidence, 1.0)
```

---

## ⚡ Performance Optimization

### Caching Strategies

#### Multi-Level Caching
```python
class MultiLevelCache:
    def __init__(self):
        self.memory_cache = {}  # Fast, temporary
        self.session_cache = st.session_state  # Session-persistent
        self.disk_cache = {}  # Persistent across sessions
    
    def get(self, key, cache_level='memory'):
        """Get cached value from specified level"""
        if cache_level == 'memory' and key in self.memory_cache:
            return self.memory_cache[key]
        
        if cache_level == 'session' and f"cache_{key}" in self.session_cache:
            return self.session_cache[f"cache_{key}"]
        
        if cache_level == 'disk':
            return self.load_from_disk(key)
        
        return None
    
    def set(self, key, value, cache_level='memory', ttl=3600):
        """Set cached value at specified level"""
        cache_entry = {
            'value': value,
            'timestamp': time.time(),
            'ttl': ttl
        }
        
        if cache_level == 'memory':
            self.memory_cache[key] = cache_entry
        elif cache_level == 'session':
            self.session_cache[f"cache_{key}"] = cache_entry
        elif cache_level == 'disk':
            self.save_to_disk(key, cache_entry)
    
    def is_valid(self, cache_entry):
        """Check if cache entry is still valid"""
        if not cache_entry:
            return False
        
        age = time.time() - cache_entry['timestamp']
        return age < cache_entry['ttl']
```

#### Intelligent Cache Invalidation
```python
class CacheInvalidator:
    def __init__(self):
        self.dependency_graph = {
            'patch_analysis': ['team_analysis', 'meta_predictions'],
            'champion_data': ['team_analysis', 'matchup_analysis'],
            'player_stats': ['player_analysis']
        }
    
    def invalidate_dependent_caches(self, changed_key):
        """Invalidate caches that depend on changed data"""
        to_invalidate = set()
        
        def find_dependents(key):
            for dependent in self.dependency_graph.get(key, []):
                to_invalidate.add(dependent)
                find_dependents(dependent)  # Recursive dependency checking
        
        find_dependents(changed_key)
        
        for cache_key in to_invalidate:
            self.clear_cache(cache_key)
    
    def clear_cache(self, key):
        """Clear specific cache entry"""
        # Clear from all cache levels
        if key in st.session_state:
            del st.session_state[key]
        
        # Clear Streamlit's built-in cache
        if hasattr(st, 'cache_data'):
            st.cache_data.clear()
```

### Async Processing

#### Background Task Management
```python
import asyncio
import concurrent.futures

class AsyncAnalysisManager:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        self.pending_tasks = {}
    
    def submit_analysis(self, analysis_type, data):
        """Submit analysis task for background processing"""
        task_id = f"{analysis_type}_{hash(str(data))}"
        
        if task_id not in self.pending_tasks:
            future = self.executor.submit(self.run_analysis, analysis_type, data)
            self.pending_tasks[task_id] = {
                'future': future,
                'start_time': time.time(),
                'analysis_type': analysis_type
            }
        
        return task_id
    
    def get_result(self, task_id):
        """Get result from background task"""
        if task_id not in self.pending_tasks:
            return None
        
        task = self.pending_tasks[task_id]
        future = task['future']
        
        if future.done():
            try:
                result = future.result()
                del self.pending_tasks[task_id]  # Clean up completed task
                return result
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                del self.pending_tasks[task_id]
                return None
        
        return 'PENDING'
    
    def run_analysis(self, analysis_type, data):
        """Run analysis in background thread"""
        # This runs in a separate thread
        return get_analysis(analysis_type, data)
```

### Request Batching

#### Batch Processing for Efficiency
```python
class BatchProcessor:
    def __init__(self, batch_size=5, timeout=2.0):
        self.batch_size = batch_size
        self.timeout = timeout
        self.pending_requests = []
        self.last_batch_time = time.time()
    
    def add_request(self, request_data):
        """Add request to batch queue"""
        self.pending_requests.append(request_data)
        
        # Process batch if size limit reached or timeout exceeded
        if (len(self.pending_requests) >= self.batch_size or 
            time.time() - self.last_batch_time > self.timeout):
            return self.process_batch()
        
        return None
    
    def process_batch(self):
        """Process accumulated requests as a batch"""
        if not self.pending_requests:
            return []
        
        batch = self.pending_requests.copy()
        self.pending_requests.clear()
        self.last_batch_time = time.time()
        
        # Combine requests into single API call
        combined_prompt = self.combine_requests(batch)
        response = self.make_batch_api_call(combined_prompt)
        
        # Split response back into individual results
        return self.split_batch_response(response, len(batch))
    
    def combine_requests(self, requests):
        """Combine multiple requests into single prompt"""
        combined = "Process the following analysis requests:\n\n"
        
        for i, request in enumerate(requests):
            combined += f"Request {i+1}:\n"
            combined += f"Type: {request['type']}\n"
            combined += f"Data: {json.dumps(request['data'])}\n\n"
        
        combined += "Provide responses in the same order as JSON array."
        return combined
```

---

## 🛡️ Error Handling

### Graceful Degradation

#### Fallback Strategies
```python
class FallbackManager:
    def __init__(self):
        self.fallback_hierarchy = {
            'team_analysis': [
                self.ai_analysis,
                self.rule_based_analysis,
                self.static_analysis
            ],
            'patch_analysis': [
                self.gemini_analysis,
                self.cached_analysis,
                self.default_analysis
            ]
        }
    
    def get_analysis_with_fallback(self, analysis_type, data):
        """Try analysis methods in order until one succeeds"""
        methods = self.fallback_hierarchy.get(analysis_type, [])
        
        for method in methods:
            try:
                result = method(data)
                if self.validate_result(result):
                    return result
            except Exception as e:
                st.warning(f"Analysis method failed: {e}")
                continue
        
        # If all methods fail, return minimal fallback
        return self.get_minimal_fallback(analysis_type)
    
    def rule_based_analysis(self, data):
        """Simple rule-based analysis as fallback"""
        # Implement basic heuristics
        team_comp = data.get('team_composition', [])
        
        analysis = {
            'summary': f"Basic analysis for {len(team_comp)} champions",
            'strengths': self.identify_basic_strengths(team_comp),
            'weaknesses': self.identify_basic_weaknesses(team_comp),
            'win_conditions': self.basic_win_conditions(team_comp)
        }
        
        return analysis
    
    def identify_basic_strengths(self, team_comp):
        """Identify strengths using simple rules"""
        strengths = []
        
        # Check for tank presence
        tanks = ['Malphite', 'Nautilus', 'Leona', 'Braum']
        if any(champ in tanks for champ in team_comp):
            strengths.append("Strong frontline presence")
        
        # Check for ADC presence
        adcs = ['Jinx', 'Caitlyn', 'Lucian', 'Vayne']
        if any(champ in adcs for champ in team_comp):
            strengths.append("Reliable damage output")
        
        return strengths or ["Balanced team composition"]
```

### Error Recovery

#### Automatic Retry Logic
```python
class RetryManager:
    def __init__(self, max_retries=3, backoff_factor=2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def retry_with_backoff(self, func, *args, **kwargs):
        """Retry function with exponential backoff"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries - 1:
                    wait_time = self.backoff_factor ** attempt
                    st.info(f"Retrying in {wait_time} seconds... (Attempt {attempt + 1})")
                    time.sleep(wait_time)
                else:
                    st.error(f"All retry attempts failed: {e}")
        
        raise last_exception
    
    def smart_retry(self, func, error_handlers=None):
        """Retry with error-specific handling"""
        error_handlers = error_handlers or {}
        
        for attempt in range(self.max_retries):
            try:
                return func()
            except Exception as e:
                error_type = type(e).__name__
                
                if error_type in error_handlers:
                    handler_result = error_handlers[error_type](e, attempt)
                    if handler_result == 'STOP':
                        break
                    elif handler_result == 'CONTINUE':
                        continue
                
                if attempt == self.max_retries - 1:
                    raise e
```

---

## 🚀 Advanced Techniques

### Model Ensemble Methods

#### Response Aggregation
```python
class ModelEnsemble:
    def __init__(self, models):
        self.models = models
        self.weights = {model: 1.0 for model in models}
    
    def ensemble_analysis(self, analysis_type, data):
        """Get analysis from multiple models and combine results"""
        responses = {}
        
        # Get responses from all models
        for model_name, model_client in self.models.items():
            try:
                response = model_client.get_analysis(analysis_type, data)
                responses[model_name] = response
            except Exception as e:
                st.warning(f"Model {model_name} failed: {e}")
        
        if not responses:
            raise Exception("All models failed")
        
        # Combine responses
        return self.combine_responses(responses, analysis_type)
    
    def combine_responses(self, responses, analysis_type):
        """Combine multiple model responses intelligently"""
        if len(responses) == 1:
            return list(responses.values())[0]
        
        combined = {}
        
        # Combine string fields (take highest confidence)
        for field in ['summary', 'playstyle']:
            field_responses = [r.get(field, '') for r in responses.values()]
            combined[field] = self.select_best_text_response(field_responses)
        
        # Combine list fields (merge and deduplicate)
        for field in ['strengths', 'weaknesses', 'win_conditions']:
            all_items = []
            for response in responses.values():
                all_items.extend(response.get(field, []))
            
            combined[field] = self.deduplicate_and_rank(all_items)
        
        return combined
    
    def select_best_text_response(self, responses):
        """Select best text response based on length and specificity"""
        if not responses:
            return ""
        
        # Score responses
        scored_responses = []
        for response in responses:
            score = len(response)  # Longer is often better
            score += response.count('specific') * 10  # Reward specificity
            score += response.count('champion') * 5   # Reward champion mentions
            scored_responses.append((score, response))
        
        # Return highest scoring response
        return max(scored_responses, key=lambda x: x[0])[1]
```

### Dynamic Prompt Adaptation

#### Context-Aware Prompt Modification
```python
class AdaptivePromptGenerator:
    def __init__(self):
        self.prompt_templates = {}
        self.performance_history = {}
    
    def generate_adaptive_prompt(self, base_template, context, task_type):
        """Generate prompt adapted to context and past performance"""
        # Start with base template
        prompt = base_template
        
        # Adapt based on context
        prompt = self.adapt_for_context(prompt, context)
        
        # Adapt based on performance history
        prompt = self.adapt_for_performance(prompt, task_type)
        
        # Adapt based on user feedback
        prompt = self.adapt_for_feedback(prompt, task_type)
        
        return prompt
    
    def adapt_for_context(self, prompt, context):
        """Adapt prompt based on current context"""
        adaptations = []
        
        # Skill level adaptation
        if context.get('player_rank') in ['IRON', 'BRONZE', 'SILVER']:
            adaptations.append(
                "Focus on fundamental concepts and avoid overly complex strategies."
            )
        elif context.get('player_rank') in ['DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']:
            adaptations.append(
                "Provide advanced, nuanced analysis suitable for high-level play."
            )
        
        # Meta adaptation
        if context.get('patch_age_days', 0) < 7:
            adaptations.append(
                "Consider that this is a new patch and meta may still be developing."
            )
        
        # Regional adaptation
        if context.get('region') in ['KR', 'CN']:
            adaptations.append(
                "Consider the aggressive, early-game focused playstyle common in this region."
            )
        
        if adaptations:
            adaptation_text = "\n".join(adaptations)
            prompt += f"\n\nAdditional Context:\n{adaptation_text}"
        
        return prompt
    
    def adapt_for_performance(self, prompt, task_type):
        """Adapt prompt based on past performance"""
        history = self.performance_history.get(task_type, [])
        
        if not history:
            return prompt
        
        # Calculate average performance
        avg_performance = sum(history) / len(history)
        
        if avg_performance < 0.7:  # Poor performance
            # Add more specific instructions
            prompt += "\n\nPlease be extra specific and detailed in your analysis."
            prompt += "\nProvide concrete examples and actionable recommendations."
        
        return prompt
    
    def update_performance(self, task_type, performance_score):
        """Update performance history for adaptive learning"""
        if task_type not in self.performance_history:
            self.performance_history[task_type] = []
        
        self.performance_history[task_type].append(performance_score)
        
        # Keep only recent history
        if len(self.performance_history[task_type]) > 20:
            self.performance_history[task_type] = self.performance_history[task_type][-20:]
```

### Real-time Model Fine-tuning

#### Feedback-Based Improvement
```python
class FeedbackLearningSystem:
    def __init__(self):
        self.feedback_data = []
        self.prompt_variations = {}
    
    def collect_feedback(self, analysis_id, user_rating, user_comments):
        """Collect user feedback on analysis quality"""
        feedback_entry = {
            'analysis_id': analysis_id,
            'rating': user_rating,
            'comments': user_comments,
            'timestamp': datetime.now(),
            'context': st.session_state.get('last_analysis_context', {})
        }
        
        self.feedback_data.append(feedback_entry)
        self.update_prompt_effectiveness()
    
    def update_prompt_effectiveness(self):
        """Update prompt effectiveness based on feedback"""
        # Group feedback by prompt characteristics
        prompt_performance = {}
        
        for feedback in self.feedback_data:
            context = feedback['context']
            prompt_key = self.generate_prompt_key(context)
            
            if prompt_key not in prompt_performance:
                prompt_performance[prompt_key] = []
            
            prompt_performance[prompt_key].append(feedback['rating'])
        
        # Update effectiveness scores
        for prompt_key, ratings in prompt_performance.items():
            avg_rating = sum(ratings) / len(ratings)
            self.prompt_variations[prompt_key] = {
                'effectiveness': avg_rating,
                'sample_size': len(ratings)
            }
    
    def get_best_prompt_variation(self, context):
        """Get the most effective prompt variation for given context"""
        prompt_key = self.generate_prompt_key(context)
        
        # Find similar prompt variations
        similar_variations = []
        for key, data in self.prompt_variations.items():
            similarity = self.calculate_context_similarity(prompt_key, key)
            if similarity > 0.7:  # Threshold for similarity
                similar_variations.append((key, data, similarity))
        
        if not similar_variations:
            return None  # Use default prompt
        
        # Weight by effectiveness and similarity
        best_variation = max(
            similar_variations,
            key=lambda x: x[1]['effectiveness'] * x[2]
        )
        
        return best_variation[0]
    
    def generate_prompt_key(self, context):
        """Generate a key representing prompt context characteristics"""
        key_components = [
            context.get('analysis_type', 'unknown'),
            context.get('player_rank', 'unranked'),
            context.get('region', 'unknown'),
            str(len(context.get('team_composition', [])))
        ]
        
        return '|'.join(key_components)
```

---

## 📊 Performance Monitoring

### Model Performance Tracking

#### Response Quality Metrics
```python
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'response_times': [],
            'success_rates': {},
            'quality_scores': {},
            'user_satisfaction': []
        }
    
    def track_response_time(self, model_name, response_time):
        """Track API response times"""
        if model_name not in self.metrics['response_times']:
            self.metrics['response_times'][model_name] = []
        
        self.metrics['response_times'][model_name].append({
            'time': response_time,
            'timestamp': datetime.now()
        })
    
    def track_success_rate(self, model_name, success):
        """Track API success rates"""
        if model_name not in self.metrics['success_rates']:
            self.metrics['success_rates'][model_name] = {'success': 0, 'total': 0}
        
        self.metrics['success_rates'][model_name]['total'] += 1
        if success:
            self.metrics['success_rates'][model_name]['success'] += 1
    
    def calculate_quality_score(self, response, expected_schema):
        """Calculate response quality score"""
        score = 0.0
        max_score = 100.0
        
        # Schema compliance (40 points)
        validation_errors = validate_response_structure(response, expected_schema)
        schema_score = max(0, 40 - len(validation_errors) * 10)
        score += schema_score
        
        # Content richness (30 points)
        content_score = self.assess_content_richness(response)
        score += content_score
        
        # Specificity (30 points)
        specificity_score = self.assess_specificity(response)
        score += specificity_score
        
        return min(score, max_score)
    
    def assess_content_richness(self, response):
        """Assess richness of response content"""
        score = 0
        
        # Check for detailed explanations
        for field, value in response.items():
            if isinstance(value, str) and len(value) > 50:
                score += 5
            elif isinstance(value, list) and len(value) >= 3:
                score += 5
        
        return min(score, 30)
    
    def assess_specificity(self, response):
        """Assess specificity of recommendations"""
        score = 0
        
        # Look for specific terms
        specific_terms = [
            'champion', 'item', 'ability', 'level', 'minute',
            'objective', 'ward', 'gank', 'roam', 'teamfight'
        ]
        
        response_text = json.dumps(response).lower()
        
        for term in specific_terms:
            if term in response_text:
                score += 2
        
        return min(score, 30)
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {},
            'detailed_metrics': self.metrics
        }
        
        # Calculate summary statistics
        for model_name, times in self.metrics['response_times'].items():
            if times:
                avg_time = sum(t['time'] for t in times) / len(times)
                report['summary'][f'{model_name}_avg_response_time'] = avg_time
        
        for model_name, rates in self.metrics['success_rates'].items():
            if rates['total'] > 0:
                success_rate = rates['success'] / rates['total']
                report['summary'][f'{model_name}_success_rate'] = success_rate
        
        return report
```

This comprehensive documentation covers the theoretical foundations and practical implementation of language models in our League of Legends analysis application. The multi-model approach, advanced prompt engineering, and robust error handling ensure reliable, high-quality analysis for users at all skill levels.