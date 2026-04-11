import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(4, "Snowpark ML & Model Development", "10:55 - 11:25 AM", "30 min", "Feature engineering view, ML classification model, evaluation metrics")

render_technologies_used([
    {"name": "Snowflake ML Classification", "description": "Built-in AutoML that trains, tunes, and evaluates classification models entirely within Snowflake. No external tools or data movement required.", "icon": "model_training"},
    {"name": "Feature Engineering Views", "description": "SQL views that transform raw operational data into ML-ready features. Views are computed on-the-fly so features always reflect the latest data.", "icon": "transform"},
    {"name": "Model Registry", "description": "Snowflake's native model registry stores trained models as first-class objects. Models can be called with SQL (MODEL!PREDICT) for inference.", "icon": "inventory_2"},
])


PROMPT_4_1 = """In PORT_AI_DEMO.PORT_OPS, create a view called CONGESTION_FEATURES that joins CONTAINER_MANIFESTS with TERMINALS and builds features for predicting whether actual_berth_time_hours will exceed estimated_berth_time_hours by more than 20%. Include these features:

- container_count, teu_count, weight_tonnes, declared_value_cad
- terminal_type (from TERMINALS)
- num_berths (from TERMINALS) 
- cargo_category
- arrival_month (extracted from arrival_date)
- arrival_day_of_week
- is_peak_season (1 if month in 10,11,12 else 0)
- cbsa_declaration_status
- A target column called IS_CONGESTED (1 if actual_berth_time_hours > estimated_berth_time_hours * 1.2, else 0)

Only include rows where both actual and estimated berth times are not null. Execute the SQL, then show me the feature distribution: count of congested vs not congested, and the average values of key features for each class."""

render_prompt("Prompt 4.1", "Feature Engineering View", PROMPT_4_1)

render_explanation("What this prompt does", """
This creates a **feature engineering view** - the bridge between raw operational data and ML model training:

**Feature selection rationale**:
- `container_count`, `teu_count`, `weight_tonnes` - Larger shipments take longer to unload
- `terminal_type`, `num_berths` - Terminal capacity affects congestion
- `cargo_category` - Some cargo types (e.g., chemicals) require special handling
- `arrival_month`, `is_peak_season` - Seasonal patterns (Oct-Dec is Asia-Pacific peak)
- `cbsa_declaration_status` - Customs holds can delay berth clearance

**Target variable**: `IS_CONGESTED` is a binary classification label. We define congestion as actual berth time exceeding estimated time by more than 20%. This is a **supervised learning** problem.

**Why a view instead of a table**: Views are dynamic - they always reflect the current data. If new manifests are inserted, the view automatically includes them. This is important for the dynamic table scoring pipeline we build in Session 5.

**Feature engineering patterns in SQL**:
```sql
EXTRACT(MONTH FROM arrival_date) AS arrival_month,
DAYOFWEEK(arrival_date) AS arrival_day_of_week,
CASE WHEN EXTRACT(MONTH FROM arrival_date) IN (10,11,12) THEN 1 ELSE 0 END AS is_peak_season
```
""")


PROMPT_4_2 = """In PORT_AI_DEMO.PORT_OPS, use Snowpark ML to train a classification model to predict IS_CONGESTED from our CONGESTION_FEATURES view. Write and execute a Snowflake SQL script that:

1. Creates a TRAIN_DATA and TEST_DATA split (80/20) from CONGESTION_FEATURES using a random seed
2. Uses Snowflake's built-in ML Classification:
   
   CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION PORT_CONGESTION_MODEL(
     INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'CONGESTION_FEATURES_TRAIN'),
     TARGET_COLNAME => 'IS_CONGESTED',
     CONFIG_OBJECT => {'on_error': 'skip'}
   );

First create the train/test views, then train the model, then run predictions on the test set and show the confusion matrix results (predicted vs actual counts). Also show the feature importances if available."""

render_prompt("Prompt 4.2", "Train a Classification Model", PROMPT_4_2)

render_explanation("What this prompt does", """
This trains a **classification model** using Snowflake's built-in ML:

**Train/Test Split**: We create two views that randomly partition the data:
```sql
CREATE VIEW CONGESTION_FEATURES_TRAIN AS
  SELECT * FROM CONGESTION_FEATURES SAMPLE (80) SEED(42);
CREATE VIEW CONGESTION_FEATURES_TEST AS
  SELECT * FROM CONGESTION_FEATURES
  WHERE manifest_id NOT IN (SELECT manifest_id FROM CONGESTION_FEATURES_TRAIN);
```

**Snowflake ML Classification**: This is Snowflake's AutoML offering:
- Automatically handles categorical encoding (one-hot for cargo_category, etc.)
- Tries multiple algorithms (gradient boosting, random forest, etc.)
- Performs hyperparameter tuning
- Stores the best model as a first-class Snowflake object

**`SYSTEM$REFERENCE`**: This function creates a secure reference to a database object. It's required when passing tables/views to ML functions to ensure proper access control.

**Model as an object**: After training, `PORT_CONGESTION_MODEL` becomes a callable object in Snowflake. You invoke it with `PORT_CONGESTION_MODEL!PREDICT(...)`. This is fundamentally different from traditional ML where you need to export models, deploy them to serving infrastructure, and manage versioning separately.
""")


PROMPT_4_3 = """Using the PORT_CONGESTION_MODEL we just trained in PORT_AI_DEMO.PORT_OPS:

1. Run predictions on the test data view and store results in a table called CONGESTION_PREDICTIONS
2. Calculate and display:
   - Overall accuracy
   - Precision and recall for the congested class
   - A confusion matrix showing TP, FP, TN, FN counts
3. Show the evaluation metrics from the model object itself using PORT_CONGESTION_MODEL!SHOW_EVALUATION_METRICS()
4. Show feature importances using PORT_CONGESTION_MODEL!SHOW_FEATURE_IMPORTANCE()

Execute all SQL and show results."""

render_prompt("Prompt 4.3", "Evaluate the Model", PROMPT_4_3)

render_explanation("What this prompt does", """
Model evaluation using both manual SQL calculations and built-in model methods:

**Manual evaluation** builds a confusion matrix:
- **True Positives (TP)**: Correctly predicted congestion
- **False Positives (FP)**: Predicted congestion but wasn't (false alarm)
- **True Negatives (TN)**: Correctly predicted no congestion
- **False Negatives (FN)**: Missed actual congestion (dangerous)

**Accuracy** = (TP + TN) / Total. But accuracy alone is misleading if classes are imbalanced.

**Precision** = TP / (TP + FP). "Of all predicted congestion events, how many actually happened?"

**Recall** = TP / (TP + FN). "Of all actual congestion events, how many did we catch?"

For port operations, **recall is more important** than precision - missing a congestion event (FN) causes delays affecting the entire supply chain, while a false alarm just means extra resources were pre-staged.

**Built-in methods**:
- `MODEL!SHOW_EVALUATION_METRICS()` - Returns AUC, F1, log loss, and more
- `MODEL!SHOW_FEATURE_IMPORTANCE()` - Shows which features the model relies on most
""")


render_key_concepts([
    {"term": "Snowflake ML Classification", "definition": "Snowflake's built-in AutoML for binary and multi-class classification. It automatically handles feature encoding, model selection, hyperparameter tuning, and evaluation. Models are stored as first-class Snowflake objects."},
    {"term": "Feature Engineering", "definition": "The process of transforming raw data into features that better represent the underlying problem for ML models. Good features are often more important than complex algorithms."},
    {"term": "SYSTEM$REFERENCE", "definition": "A Snowflake system function that creates a secure, permissions-aware reference to a database object. Required when passing tables or views to ML training functions."},
    {"term": "Confusion Matrix", "definition": "A 2x2 table showing True Positives, False Positives, True Negatives, and False Negatives. The foundation for calculating precision, recall, F1 score, and other classification metrics."},
])

render_domain_glossary([
    {"term": "Berth Time", "definition": "The time a vessel spends moored at a terminal berth for loading/unloading. Estimated berth time is planned; actual berth time includes delays. The gap between them is our congestion signal."},
    {"term": "Port Congestion", "definition": "When vessel demand exceeds terminal capacity, ships wait at anchor (in English Bay or at Roberts Bank anchorage) before berthing. Congestion ripples through the entire supply chain — rail delays, trucking bottlenecks, and inventory shortages."},
    {"term": "Peak Asia-Pacific Trade Season", "definition": "October through December sees the highest cargo volumes as retailers stock up for holiday season. Trans-Pacific shipping volumes can increase 20-30% above baseline during Q4."},
])

render_what_you_built([
    "CONGESTION_FEATURES view with 10+ engineered features",
    "Train/test data split views (80/20)",
    "PORT_CONGESTION_MODEL - trained classification model",
    "CONGESTION_PREDICTIONS table with scored test data",
    "Evaluation metrics: accuracy, precision, recall, confusion matrix",
])
