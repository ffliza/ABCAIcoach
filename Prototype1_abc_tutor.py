#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:45:36 2026

@author: farhanaadmin

This code works well with progress log. 

"""

import streamlit as st
import numpy as np
import re
import os
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime
import plotly.express as px
import random
import time
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Distress Tolerance Assistant",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .skill-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_skill' not in st.session_state:
    st.session_state.current_skill = "STOP"
if 'emotion_logs' not in st.session_state:
    st.session_state.emotion_logs = []
if 'practice_reminders' not in st.session_state:
    st.session_state.practice_reminders = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'api_choice' not in st.session_state:
    st.session_state.api_choice = "Groq Cloud"

class DistressToleranceAPI:
    """RAG model using Llama via public APIs"""
    
    def __init__(self, api_choice: str, api_key: str):
        self.api_choice = api_choice
        self.api_key = api_key
        self.document_content = self.get_document_content()
        
    def get_document_content(self) -> str:
        """Get the full document content."""
        return """
        DISTRESS TOLERANCE SKILLS - COMPLETE GUIDE
        
        STOP Skill:
        The STOP skill helps you respond instead of react when Emotion Mind takes over.
        
        Step 1 - Stop: Freeze when emotions take over. Don't move a muscle. This prevents impulsive action.
        Step 2 - Take a step back: Physically and mentally pause. Take a deep breath. Leave the room if needed.
        Step 3 - Observe: Look at facts without judgment. Ask: What's really happening? What am I responding to?
        Step 4 - Proceed mindfully: Use Wise Mind to decide next step. Ask: What's the most helpful action now?
        
        Example: A friend shouts at you. Instead of shouting back, STOP, take a breath, observe what's happening, then respond calmly.
        
        TIPP Skills (for overwhelming emotions when you're in the "red zone"):
        
        Tip Temperature: Put cold water on your face for 10-20 seconds. This activates the dive reflex, slowing your heart rate. You can also use an ice pack on your cheeks.
        
        Intense Exercise: Do aerobic exercise for 10-20 minutes. Examples: running, swimming, jumping jacks, dancing, power walking, push-ups. This burns off stress energy.
        
        Paced Breathing: Slow your breathing to 5-6 breaths per minute. Inhale for 4 seconds, exhale for 6-8 seconds. Place your hand on your belly to feel the breath.
        
        Progressive Muscle Relaxation: Tense each muscle group for 10 seconds, then relax for 10 seconds. Work from head to toe: forehead, eyes, nose, neck, shoulders, chest, fists, stomach, buttocks, legs, feet.
        
        These skills work fast (5-20 minutes). Use when you can't think straight or feel completely overwhelmed.
        
        Self-Soothing:
        Use your five senses plus movement to find comfort during distress.
        
        Sight: Watch clouds, look at photos, draw, color, people-watch, look at posters, watch nature videos.
        Hearing: Listen to calming music, nature sounds (birds, rain, ocean), play an instrument, listen to ASMR or white noise.
        Smell: Use scented lotions, light a candle, bake cookies, make coffee or tea, use essential oils, smell flowers.
        Taste: Eat favorite food slowly, drink hot chocolate or tea, suck on a mint, really notice what you're eating.
        Touch: Take a warm bath or shower, pet an animal, get a massage, brush your hair, use soft blankets, hold a stress ball.
        Movement: Stretch, go for a walk, dance, practice yoga, play a sport, do gentle exercises.
        
        Create a "self-soothe box" with comforting items: coloring books, photos of loved ones, puzzle books, music, fidget toys, soft socks, sour candy, hot chocolate, hand cream, lavender bag.
        
        IMPROVE the Moment:
        These skills change your internal experience when distressed.
        
        Imagery: Imagine a relaxing scene (beach, forest, mountains). Imagine yourself coping well and handling the situation. Imagine things going well.
        
        Meaning: Find purpose or meaning in painful situations. Examples: Use your experience to help others. A bad test grade leads to extra help from a caring teacher. Caring for a sick relative reunites estranged family members.
        
        Patience: Remember that no feeling lasts forever. Don't wish your time away. Let feelings come and go without judgment.
        
        Relaxation: Listen to guided relaxation, stretch, take a bath, get a massage, do deep breathing.
        
        One thing in the moment: Focus all attention on ONE thing you're doing. Do that thing mindfully without multitasking.
        
        Vacation: Take a few moments for yourself. Do something different. Go for a walk. Read a book. Unplug from electronics for an hour.
        
        Encouragement: Cheerlead yourself with positive statements: "I can do this." "It won't last forever." "I'm doing the best I can." "I've gotten through hard times before."
        
        Radical Acceptance:
        Accepting things you cannot change to reduce suffering.
        
        What it is: Accepting reality as it is (not fighting it). Acknowledging what happened without judgment. Reducing suffering when you can't solve the problem.
        
        What it is NOT: Approval of the situation. Forgiveness. Condoning behaviors. Giving up. Never asserting yourself.
        
        Wilfulness vs Willingness:
        - Wilfulness: "It shouldn't be this way!" "Why me?" Fighting reality. Refusing to tolerate the situation.
        - Willingness: "It is what it is." Accepting reality. Doing what works. Using appropriate skills.
        
        To practice radical acceptance: Notice when you're fighting reality. Turn your mind toward acceptance (you may need to do this many times). Say "I accept this moment as it is."
        
        Pros and Cons:
        Make wise decisions by weighing options before a crisis hits.
        
        Steps:
        1. Think of a situation where you have crisis urges
        2. List pros AND cons of acting on the urge
        3. List pros AND cons of resisting the urge
        4. Consider short-term AND long-term consequences
        5. Keep this list to review when urges strike
        
        Example for drug use:
        Acting on urge pros: Distraction, feel positive (short-term), escape feelings
        Acting on urge cons: More impulsive, alienate friends (long-term), comedown, neglect health
        Resisting urge pros: Less impulsivity, more money, pride, clearer brain, sense of accomplishment
        Resisting urge cons: No elation, feel deprived, still face difficult situation
        
        Remember: Acting on urges might feel good now but often leads to negative long-term consequences.
        """
    
    def get_relevant_context(self, query: str) -> str:
        """Extract relevant context based on keywords."""
        query_lower = query.lower()
        
        sections = []
        
        if "stop" in query_lower:
            sections.append(self.get_stop_section())
        if "tipp" in query_lower or "temperature" in query_lower or "exercise" in query_lower or "breathing" in query_lower:
            sections.append(self.get_tipp_section())
        if "self-soothe" in query_lower or "self soothe" in query_lower or "senses" in query_lower:
            sections.append(self.get_self_soothe_section())
        if "improve" in query_lower or "imagery" in query_lower or "meaning" in query_lower or "patience" in query_lower:
            sections.append(self.get_improve_section())
        if "radical acceptance" in query_lower or "acceptance" in query_lower or "accept" in query_lower:
            sections.append(self.get_acceptance_section())
        if "pros and cons" in query_lower or "pros" in query_lower or "cons" in query_lower:
            sections.append(self.get_pros_cons_section())
        
        if not sections:
            return self.get_general_overview()
        
        return "\n\n".join(sections)
    
    def get_stop_section(self) -> str:
        return """STOP Skill:
The STOP skill helps you respond instead of react when Emotion Mind takes over.

S - Stop: Freeze when emotions take over. Don't move a muscle.
T - Take a step back: Physically and mentally pause. Leave the room if needed.
O - Observe: Look at facts without judgment. What's really happening?
P - Proceed mindfully: Use Wise Mind to decide the most helpful next step.

Example: A friend shouts at you. Instead of shouting back, STOP, take a breath, observe, then respond calmly."""
    
    def get_tipp_section(self) -> str:
        return """TIPP Skills (for overwhelming emotions when you're in the "red zone"):

Tip Temperature: Put cold water on your face for 10-20 seconds. Activates dive reflex, slowing heart rate.

Intense Exercise: Do aerobic exercise for 10-20 minutes: running, jumping jacks, dancing, power walking.

Paced Breathing: Inhale for 4 seconds, exhale for 6-8 seconds. Repeat for 1-2 minutes.

Progressive Muscle Relaxation: Tense each muscle group for 10 seconds, then relax for 10 seconds. Work from head to toe.

These skills work fast (5-20 minutes). Use when you can't think straight."""
    
    def get_self_soothe_section(self) -> str:
        return """Self-Soothing - Using your five senses plus movement:

Sight: Watch clouds, look at photos, draw, color, people-watch
Hearing: Listen to calming music, nature sounds, play instrument
Smell: Use scented lotions, light a candle, bake cookies, make coffee
Taste: Eat favorite food slowly, drink hot chocolate, suck on a mint
Touch: Warm bath, pet an animal, soft blankets, stress ball, massage
Movement: Stretch, walk, dance, yoga, gentle exercise

Create a "self-soothe box" with comforting items."""
    
    def get_improve_section(self) -> str:
        return """IMPROVE the Moment:

Imagery: Imagine a relaxing scene or yourself coping well
Meaning: Find purpose in pain - use experience to help others
Patience: No feeling lasts forever. Let feelings come and go
Relaxation: Stretch, take a bath, get a massage, deep breathing
One thing: Focus mindfully on ONE activity without multitasking
Vacation: Take a mental break, read, walk, unplug from electronics
Encouragement: Positive self-talk - "I can do this" "This will pass"""
    
    def get_acceptance_section(self) -> str:
        return """Radical Acceptance:

What it is: Accepting reality as it is without fighting it. Reducing suffering when you can't solve the problem.

What it is NOT: Approval, forgiveness, giving up, or condoning behavior.

Wilfulness: "It shouldn't be this way!" "Why me?" - Fighting reality
Willingness: "It is what it is" - Accepting and moving forward

To practice: Notice when you're fighting reality. Turn your mind toward acceptance. Say "I accept this moment as it is."
"""
    
    def get_pros_cons_section(self) -> str:
        return """Pros and Cons:

Steps:
1. Think of a situation with crisis urges
2. List pros AND cons of acting on the urge
3. List pros AND cons of resisting the urge
4. Consider short-term AND long-term consequences

Example for drug use:
Acting on urge pros: Distraction, feel positive (short-term)
Acting on urge cons: More impulsive, alienate friends (long-term), health issues
Resisting urge pros: Less impulsivity, pride, clearer brain
Resisting urge cons: No elation, still face difficult situation"""
    
    def get_general_overview(self) -> str:
        return """Distress Tolerance Skills Overview:

1. STOP: Stop, Take a step back, Observe, Proceed mindfully
2. TIPP: Tip temperature, Intense exercise, Paced breathing, Progressive relaxation
3. Self-soothing: Use sight, hearing, smell, taste, touch, and movement
4. IMPROVE: Imagery, Meaning, Patience, Relaxation, One thing, Vacation, Encouragement
5. Radical Acceptance: Accept what you cannot change
6. Pros and Cons: Weigh acting on urges vs resisting

These skills help you survive crisis situations without making things worse."""
    
    def call_llama_api(self, prompt: str, model_tier: str = "balanced") -> str:
        """Call Llama via public API."""
        
        if self.api_choice == "Groq Cloud":
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Use working model
            payload = {
                "model": "llama-3.3-70b-versatile", # "mixtral-8x7b-32768",  # Stable, working model
                "messages": [
                    {"role": "system", "content": "You are a Distress Tolerance assistant. Only answer based on the provided context. Be helpful, concise, and compassionate."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                else:
                    error_msg = f"API Error: {response.status_code}"
                    try:
                        error_detail = response.json()
                        error_msg += f" - {error_detail.get('error', {}).get('message', response.text)}"
                    except:
                        error_msg += f" - {response.text}"
                    
                    st.error(error_msg)
                    return self._fallback_response(prompt)
                    
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
                return self._fallback_response(prompt)
        
        elif self.api_choice == "Together.ai":
            url = "https://api.together.xyz/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "meta-llama/Llama-3.2-3B-Instruct-Turbo",
                "messages": [
                    {"role": "system", "content": "You are a Distress Tolerance assistant. Only answer based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                else:
                    st.error(f"Together.ai Error: {response.status_code} - {response.text}")
                    return self._fallback_response(prompt)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                return self._fallback_response(prompt)
        
        else:
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response using keyword matching."""
        if "STOP" in prompt:
            return self.get_stop_section()
        elif "TIPP" in prompt:
            return self.get_tipp_section()
        elif "self-soothe" in prompt.lower():
            return self.get_self_soothe_section()
        elif "IMPROVE" in prompt:
            return self.get_improve_section()
        elif "Radical Acceptance" in prompt:
            return self.get_acceptance_section()
        elif "Pros and Cons" in prompt:
            return self.get_pros_cons_section()
        else:
            return self.get_general_overview()
    
    def answer(self, query: str) -> Dict[str, Any]:
        """Answer based on document using Llama API."""
        
        context = self.get_relevant_context(query)
        
        prompt = f"""CONTEXT from Distress Tolerance Document:
{context}

USER QUESTION: {query}

INSTRUCTIONS:
1. ONLY use information from the CONTEXT above
2. If the answer is NOT in the CONTEXT, say: "I can only answer questions about Distress Tolerance skills (STOP, TIPP, Self-soothing, IMPROVE, Radical Acceptance, Pros and Cons)."
3. Be helpful, clear, and compassionate

YOUR ANSWER:"""
        
        answer = self.call_llama_api(prompt)
        
        return {
            "answer": answer,
            "context_used": context
        }

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4351/4351051.png", width=80)
    st.title("Distress Tolerance")
    st.markdown("---")
    
    # API Configuration
    st.subheader("API Configuration")
    
    api_choice = st.selectbox(
        "Choose Llama API Provider:",
        ["Groq Cloud", "Together.ai"]
    )
    
    api_key = st.text_input(
        "API Key:",
        type="password",
        placeholder="Enter your API key",
        help="Get a free API key from groq.com or together.ai"
    )
    
    if api_key:
        st.session_state.api_key = api_key
        st.session_state.api_choice = api_choice
        
        if st.button("Test Connection"):
            test_model = DistressToleranceAPI(api_choice, api_key)
            test_response = test_model.call_llama_api("What is the STOP skill?")
            if "STOP" in test_response or "stop" in test_response.lower():
                st.success("Connection successful!")
            else:
                st.error("Connection failed. Check your API key.")
    
    st.markdown("---")
    
    # Navigation menu
    menu = st.radio(
        "Navigation",
        ["Chat Assistant", "Skills Library", "My Progress", "Practice Tools", "About"]
    )
    
    st.markdown("---")
    
    st.subheader("Quick Skills")
    skill = st.selectbox(
        "Select a skill to learn about:",
        ["STOP", "TIPP", "Self-soothing", "IMPROVE", "Radical Acceptance", "Pros and Cons"]
    )
    
    if st.button("Learn About " + skill):
        st.session_state.current_skill = skill
        menu = "Skills Library"
    
    st.markdown("---")
    
    st.subheader("How are you feeling?")
    emotion = st.select_slider(
        "Emotion intensity",
        options=["Calm", "Mildly upset", "Moderately distressed", "Very overwhelmed"]
    )
    
    if st.button("Log this feeling"):
        st.session_state.emotion_logs.append({
            "timestamp": datetime.now(),
            "emotion": emotion,
            "skill_used": None
        })
        st.success("Feeling logged!")
    
    st.markdown("---")
    
    st.error("**In Crisis?**")
    if st.button("Use TIPP Now", use_container_width=True):
        st.info("""
        **Quick TIPP:**
        1. Splash cold water on your face (20 sec)
        2. Do 20 jumping jacks
        3. Take 5 slow breaths (exhale longer)
        4. Tense and relax your muscles
        """)

# Main content area
if menu == "Chat Assistant":
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">Distress Tolerance Assistant</h1>
        <p style="color: white; margin: 0;">Powered by Llama API</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.api_key:
        st.warning("Please enter your API key in the sidebar to use the Llama assistant.")
        st.info("""
        **Get a free API key:**
        - **Groq Cloud**: Sign up at groq.com (free tier available)
        - **Together.ai**: Sign up at together.ai (free credits available)
        """)
    else:
        model = DistressToleranceAPI(st.session_state.api_choice, st.session_state.api_key)
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <b>You:</b><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <b>Assistant:</b><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        user_input = st.chat_input("Ask about distress tolerance skills...")
        
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("Thinking..."):
                response = model.answer(user_input)
                bot_response = response["answer"]
            
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.rerun()
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

elif menu == "Skills Library":
    st.markdown("## Skills Library")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["STOP", "TIPP", "Self-soothing", "IMPROVE", "Radical Acceptance", "Pros and Cons"]
    )
    
    with tab1:
        st.markdown("""
        <div class="skill-card">
            <h3>STOP Skill</h3>
            <p><strong>When to use:</strong> When you feel Emotion Mind taking over</p>
            <hr>
            <h4>The 4 Steps:</h4>
            <ol>
                <li><strong>S - Stop</strong> - Freeze when emotions take control</li>
                <li><strong>T - Take a step back</strong> - Physically and mentally pause</li>
                <li><strong>O - Observe</strong> - Look at facts without judgment</li>
                <li><strong>P - Proceed mindfully</strong> - Use Wise Mind to decide next step</li>
            </ol>
            <div style="background-color: #e8f5e9; padding: 1rem; border-radius: 5px; margin-top: 1rem;">
                <strong>Example:</strong> A friend shouts at you -> STOP, take a breath, observe what's happening, then respond calmly.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        situation = st.text_area("Describe a recent situation where you felt emotionally overwhelmed:")
        if st.button("Apply STOP to this situation"):
            if situation:
                st.success("Apply the 4 steps: Stop, Take a step back, Observe, Proceed mindfully")
    
    with tab2:
        st.markdown("""
        <div class="skill-card">
            <h3>TIPP Skills</h3>
            <p><strong>When to use:</strong> When emotions are overwhelming (the "red zone")</p>
            <hr>
            <h4>The 4 Components:</h4>
            <ul>
                <li><strong>Tip Temperature</strong> - Cold water on face for 10-20 seconds</li>
                <li><strong>Intense Exercise</strong> - Run, jump, dance for 10-20 minutes</li>
                <li><strong>Paced Breathing</strong> - Exhale longer than inhale (4 sec in, 6-8 out)</li>
                <li><strong>Progressive Muscle Relaxation</strong> - Tense/relax each muscle group</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        tipp_step = st.radio("Choose a TIPP skill to practice:", 
                            ["Tip Temperature", "Intense Exercise", "Paced Breathing", "Progressive Relaxation"])
        
        if tipp_step == "Tip Temperature":
            st.info("Get cold water or an ice pack. Hold your breath and place it on your cheeks for 10-20 seconds.")
        elif tipp_step == "Intense Exercise":
            st.info("Try: 20 jumping jacks, run in place for 1 minute, or dance energetically.")
        elif tipp_step == "Paced Breathing":
            st.info("Inhale for 4 seconds, exhale for 6-8 seconds. Repeat 10 times.")
        else:
            st.info("Tense each muscle group for 10 seconds, then release. Work from head to toe.")
    
    with tab3:
        st.markdown("""
        <div class="skill-card">
            <h3>Self-Soothing</h3>
            <p><strong>When to use:</strong> When Emotion Mind begins to take over</p>
            <hr>
            <h4>Using Your Senses:</h4>
            <ul>
                <li><strong>Sight:</strong> Watch clouds, look at photos, draw</li>
                <li><strong>Hearing:</strong> Listen to music, nature sounds</li>
                <li><strong>Smell:</strong> Use scented lotions, bake cookies</li>
                <li><strong>Taste:</strong> Eat favorite food slowly</li>
                <li><strong>Touch:</strong> Take warm bath, pet animal, soft blankets</li>
                <li><strong>Movement:</strong> Stretch, walk, dance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Build Your Self-Soothe Kit")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Sight items (photos, art, etc.)", key="sight")
            st.text_input("Hearing items (music, podcasts, etc.)", key="hearing")
            st.text_input("Smell items (candles, lotions, etc.)", key="smell")
        with col2:
            st.text_input("Taste items (tea, chocolate, etc.)", key="taste")
            st.text_input("Touch items (blanket, stress ball, etc.)", key="touch")
            st.text_input("Movement (yoga, walk, etc.)", key="movement")
        
        if st.button("Save My Self-Soothe Kit"):
            st.success("Self-soothe kit saved! Use these items when distressed.")
    
    with tab4:
        st.markdown("""
        <div class="skill-card">
            <h3>IMPROVE the Moment</h3>
            <h4>The 7 Techniques:</h4>
            <ul>
                <li><strong>Imagery:</strong> Imagine a calm place or yourself coping well</li>
                <li><strong>Meaning:</strong> Find purpose in pain (help others, learn lessons)</li>
                <li><strong>Patience:</strong> Remember feelings don't last forever</li>
                <li><strong>Relaxation:</strong> Stretch, take bath, get massage</li>
                <li><strong>One thing:</strong> Focus mindfully on single activity</li>
                <li><strong>Vacation:</strong> Take mental break, read, walk</li>
                <li><strong>Encouragement:</strong> Positive self-talk ("I can do this")</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Encouragement"):
            messages = ["I can do this, one step at a time", "This feeling won't last forever", 
                       "I'm doing the best I can right now", "I've gotten through difficult moments before"]
            st.success(f"Say to yourself: {random.choice(messages)}")
    
    with tab5:
        st.markdown("""
        <div class="skill-card">
            <h3>Radical Acceptance</h3>
            <p><strong>When to use:</strong> When you cannot change a painful situation</p>
            <hr>
            <h4>What It Is:</h4>
            <ul>
                <li>Accepting reality as it is (not fighting it)</li>
                <li>Reducing suffering when you can't solve the problem</li>
                <li>A choice you make, not approval or forgiveness</li>
            </ul>
            <h4>Wilfulness vs Willingness:</h4>
            <ul>
                <li><strong>Wilfulness:</strong> "It shouldn't be this way!" "Why me?"</li>
                <li><strong>Willingness:</strong> "It is what it is" (accepting and moving forward)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        struggle = st.text_area("What situation are you struggling to accept?")
        if st.button("Practice Acceptance"):
            if struggle:
                st.info("Try saying: 'I don't like this, but I accept that it's happening right now. I can handle this moment.'")
    
    with tab6:
        st.markdown("""
        <div class="skill-card">
            <h3>Pros and Cons</h3>
            <h4>How to Use:</h4>
            <ol>
                <li>Think of a situation where you have crisis urges</li>
                <li>List pros AND cons of acting on urges</li>
                <li>List pros AND cons of resisting urges</li>
                <li>Consider short-term AND long-term consequences</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        urge = st.text_input("What urge are you struggling with?")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Acting on urge**")
            st.text_area("Pros", key="pros_act")
            st.text_area("Cons", key="cons_act")
        with col2:
            st.write("**Resisting urge**")
            st.text_area("Pros", key="pros_resist")
            st.text_area("Cons", key="cons_resist")

elif menu == "My Progress":
    st.markdown("## My Progress Tracking")
    
    # Display emotion logs
    st.subheader("Emotion Check-ins")
    
    if st.session_state.emotion_logs:
        df_emotions = pd.DataFrame(st.session_state.emotion_logs)
        df_emotions['timestamp'] = pd.to_datetime(df_emotions['timestamp'])
        
        emotion_map = {"Calm": 1, "Mildly upset": 2, "Moderately distressed": 3, "Very overwhelmed": 4}
        df_emotions['intensity'] = df_emotions['emotion'].map(emotion_map)
        
        fig = px.line(df_emotions, x='timestamp', y='intensity', title="Emotion Intensity Over Time")
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Distress", f"{df_emotions['intensity'].mean():.1f}/4")
        with col2:
            st.metric("Total Check-ins", len(df_emotions))
        with col3:
            calm_count = len(df_emotions[df_emotions['intensity'] == 1])
            st.metric("Calm Moments", calm_count)
        
        st.dataframe(df_emotions[['timestamp', 'emotion']].tail(10))
    else:
        st.info("No emotion logs yet. Use the sidebar to log how you're feeling!")
    
    st.markdown("---")
    
    # Display skills practice logs
    st.subheader("Skills Practice Log")
    
    # Form for logging practice
    with st.form(key="practice_log_form"):
        col1, col2 = st.columns(2)
        with col1:
            skill_practiced = st.selectbox(
                "Which skill did you practice?", 
                ["STOP", "TIPP", "Self-soothing", "IMPROVE", "Radical Acceptance", "Pros and Cons"],
                key="practice_skill"
            )
        with col2:
            effectiveness = st.slider("How effective was it? (1-10)", 1, 10, 5, key="practice_effectiveness")
        
        notes = st.text_area("Notes (optional)", placeholder="What did you notice? How did it help?")
        
        submit_button = st.form_submit_button(label="Log Practice")
        
        if submit_button:
            # Add to practice reminders
            st.session_state.practice_reminders.append({
                "timestamp": datetime.now(),
                "skill": skill_practiced,
                "effectiveness": effectiveness,
                "notes": notes
            })
            st.success(f"✅ Logged {skill_practiced} practice! Effectiveness: {effectiveness}/10")
            st.rerun()
    
    # Display practice history
    if st.session_state.practice_reminders:
        st.markdown("### Practice History")
        
        df_practice = pd.DataFrame(st.session_state.practice_reminders)
        df_practice['timestamp'] = pd.to_datetime(df_practice['timestamp'])
        df_practice['date'] = df_practice['timestamp'].dt.date
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Practices", len(df_practice))
        with col2:
            avg_effectiveness = df_practice['effectiveness'].mean()
            st.metric("Average Effectiveness", f"{avg_effectiveness:.1f}/10")
        with col3:
            most_practiced = df_practice['skill'].mode().iloc[0] if not df_practice.empty else "None"
            st.metric("Most Practiced Skill", most_practiced)
        
        # Effectiveness by skill chart
        if len(df_practice) > 1:
            skill_effectiveness = df_practice.groupby('skill')['effectiveness'].mean().sort_values(ascending=True)
            fig2 = px.bar(skill_effectiveness, x='effectiveness', y=skill_effectiveness.index, 
                          title="Average Effectiveness by Skill", orientation='h')
            st.plotly_chart(fig2, use_container_width=True)
        
        # Practice timeline
        fig3 = px.line(df_practice, x='timestamp', y='effectiveness', 
                       title="Practice Effectiveness Over Time",
                       labels={'effectiveness': 'Effectiveness (1-10)', 'timestamp': 'Date'})
        st.plotly_chart(fig3, use_container_width=True)
        
        # Detailed history table
        st.dataframe(
            df_practice[['timestamp', 'skill', 'effectiveness', 'notes']].sort_values('timestamp', ascending=False),
            use_container_width=True
        )
        
        # Export button
        if st.button("Export Practice Data (CSV)"):
            csv = df_practice.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"distress_tolerance_practice_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Clear history button
        if st.button("Clear Practice History", type="secondary"):
            st.session_state.practice_reminders = []
            st.success("Practice history cleared!")
            st.rerun()
    else:
        st.info("No practice logs yet. Use the form above to log your skill practice!")

elif menu == "Practice Tools":
    st.markdown("## Practice Tools and Exercises")
    
    challenges = [
        "Practice STOP skill once today when you feel frustrated",
        "Try TIPP temperature skill (cold water on face) and notice the effect",
        "Create one item for your self-soothe kit",
        "Practice paced breathing for 2 minutes",
        "Use positive self-talk three times today",
        "Practice radical acceptance with a small frustration"
    ]
    
    st.subheader("Today's Challenge")
    today_challenge = random.choice(challenges)
    st.success(f"**{today_challenge}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ I completed today's challenge"):
            st.balloons()
            st.success("Great job! You're building important skills.")
            # Auto-log the practice
            st.session_state.practice_reminders.append({
                "timestamp": datetime.now(),
                "skill": "Daily Challenge",
                "effectiveness": 8,
                "notes": f"Completed: {today_challenge}"
            })
    with col2:
        if st.button("🔄 New Challenge"):
            st.rerun()
    
    st.markdown("---")
    st.subheader("Guided Exercises")
    
    exercise_type = st.radio("Choose an exercise:", 
                            ["STOP Practice", "TIPP Quick Guide", "Self-Soothe Box Planner", "Radical Acceptance Meditation"])
    
    if exercise_type == "STOP Practice":
        st.markdown("""
        **Step-by-step STOP exercise:**
        1. Find a quiet space
        2. Think of a recent triggering situation
        3. Practice: Stop -> Take a step back -> Observe -> Proceed
        4. Write down what you noticed:
        """)
        stop_reflection = st.text_area("Your reflection:", key="stop_reflection")
        if stop_reflection and st.button("Save STOP Reflection"):
            st.session_state.practice_reminders.append({
                "timestamp": datetime.now(),
                "skill": "STOP Practice",
                "effectiveness": 7,
                "notes": stop_reflection
            })
            st.success("Reflection saved to Practice Log!")
    
    elif exercise_type == "TIPP Quick Guide":
        st.code("""
        TIPP - CRISIS SURVIVAL
        
        T - TIP TEMPERATURE: Cold water on face - 20 seconds
        I - INTENSE EXERCISE: 10-20 min of running/jumping
        P - PACED BREATHING: In 4 sec -> Out 6-8 sec
        P - PROGRESSIVE RELAXATION: Tense muscles -> Release
        """)
        
        if st.button("Start 2-minute breathing exercise"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(1.2)
                progress_bar.progress(i + 1)
            st.success("Great job! Consider logging this practice.")
            
            if st.button("Log this TIPP practice"):
                st.session_state.practice_reminders.append({
                    "timestamp": datetime.now(),
                    "skill": "TIPP - Paced Breathing",
                    "effectiveness": 7,
                    "notes": "Completed 2-minute breathing exercise"
                })
                st.success("Logged to Practice History!")
    
    elif exercise_type == "Self-Soothe Box Planner":
        st.markdown("Create your personal self-soothe box with items that engage your senses:")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Sight:** Photos, coloring book, art")
            st.write("**Sound:** Music, nature sounds, instrument")
            st.write("**Smell:** Candles, lotions, baking")
        with col2:
            st.write("**Taste:** Tea, chocolate, favorite snack")
            st.write("**Touch:** Soft blanket, stress ball, lotion")
            st.write("**Movement:** Yoga mat, walking shoes")
        
        if st.button("Build My Box"):
            st.balloons()
            st.success("Gather these items and keep them accessible for when you need them!")
    
    else:
        st.markdown("""
        **Radical Acceptance Meditation** (5 minutes)
        
        Read each statement slowly:
        
        *"I accept that this moment is exactly as it is."*
        
        *"I don't have to like it to accept it."*
        
        *"Fighting reality only increases my suffering."*
        
        *"I choose to accept this moment and move forward."*
        """)
        
        if st.button("Start meditation"):
            with st.spinner("Meditating..."):
                time.sleep(5)
            st.success("Thank you for practicing.")
            
            if st.button("Log this meditation"):
                st.session_state.practice_reminders.append({
                    "timestamp": datetime.now(),
                    "skill": "Radical Acceptance Meditation",
                    "effectiveness": 7,
                    "notes": "Completed 5-minute acceptance meditation"
                })
                st.success("Logged to Practice History!")

else:
    st.markdown("""
    ## About This App
    
    ### What is Distress Tolerance?
    
    Distress tolerance skills help you survive crisis situations without making things worse. These skills are from IDEAS Distress Tolerance Module.
    
    ### Llama API Providers
    
    This app uses Llama models via:
    - **Groq Cloud**: Fastest inference, free tier available at groq.com

    
    ### Crisis Resources
    
    If you're in immediate crisis:
    - **111** - NHS Mental Health

    
    ### Important Note
    
    This app is **not a substitute for professional mental health treatment**.
    
    ---
    
    *"These skills help us to tolerate difficult situations and emotions when the problems can't be solved straight away."*
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    Distress Tolerance Assistant | Powered by Llama API | Based on DBT Skills
</div>
""", unsafe_allow_html=True)