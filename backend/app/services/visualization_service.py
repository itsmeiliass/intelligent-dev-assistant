# app/services/visualization_service.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64
from typing import Dict, Any
from datetime import datetime
from typing import List

class VisualizationService:
    def __init__(self):
        plt.style.use('default')
        sns.set_palette("husl")
    
    def create_quality_radar_chart(self, metrics: Dict[str, float]) -> str:
        """
        Crée un graphique radar pour la qualité du code
        """
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        # Compléter le cercle
        values += values[:1]
        categories += categories[:1]
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Create angles
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        
        # Draw plot
        ax.plot(angles, values, linewidth=2, linestyle='solid')
        ax.fill(angles, values, alpha=0.25)
        
        # Add labels
        ax.set_thetagrids(np.degrees(angles[:-1]), categories)
        ax.set_ylim(0, 100)
        ax.set_title("Code Quality Radar Chart", size=16, fontweight='bold')
        
        # Convert to base64
        return self._fig_to_base64(fig)
    
    def create_timeseries_plot(self, historical_data: List[Dict]) -> str:
        """
        Crée un graphique temporel des métriques
        """
        if not historical_data:
            return None
        
        # Préparer les données
        timestamps = []
        scores = []
        
        for data in historical_data:
            if "timestamp" in data and "quality_score" in data:
                timestamps.append(datetime.fromisoformat(data["timestamp"]))
                scores.append(data["quality_score"])
        
        if not timestamps:
            return None
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(timestamps, scores, marker='o', linewidth=2)
        ax.set_xlabel("Time")
        ax.set_ylabel("Quality Score")
        ax.set_title("Code Quality Over Time")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def create_comparison_bar_chart(self, current_metrics: Dict, previous_metrics: Dict) -> str:
        """
        Crée un graphique comparatif entre deux analyses
        """
        categories = list(current_metrics.keys())
        current_values = [current_metrics.get(cat, 0) for cat in categories]
        previous_values = [previous_metrics.get(cat, 0) for cat in categories]
        
        x = np.arange(len(categories))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars1 = ax.bar(x - width/2, current_values, width, label='Current', alpha=0.8)
        bars2 = ax.bar(x + width/2, previous_values, width, label='Previous', alpha=0.8)
        
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Scores')
        ax.set_title('Code Quality Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
        
        # Add value labels
        self._add_value_labels(ax, bars1)
        self._add_value_labels(ax, bars2)
        
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """Convertit une figure matplotlib en base64"""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_str}"
    
    def _add_value_labels(self, ax, bars):
        """Ajoute des labels de valeur aux barres"""
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

# Instance globale
visualization_service = VisualizationService()