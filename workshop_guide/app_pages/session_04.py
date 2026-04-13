import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(4, "Snowpark ML & Model Development", "10:55 - 11:25 AM", "30 min", "Feature engineering, ML classification, Snowflake Notebook with Feature Store & Model Registry")

render_technologies_used([
    {"name": "Snowflake ML Classification", "description": "Built-in AutoML that trains, tunes, and evaluates classification models entirely within Snowflake. No external tools or data movement required.", "icon": "model_training"},
    {"name": "Feature Engineering Views", "description": "SQL views that transform raw operational data into ML-ready features. Views are computed on-the-fly so features always reflect the latest data.", "icon": "transform"},
    {"name": "Model Registry", "description": "Snowflake's native model registry stores trained models as first-class objects. Models can be called with SQL (MODEL!PREDICT) for inference.", "icon": "inventory_2"},
    {"name": "Feature Store", "description": "Centralized feature management for ML. Register entities, create managed feature views backed by Dynamic Tables, and generate point-in-time correct training datasets.", "icon": "hub"},
    {"name": "Snowflake Notebooks", "description": "Interactive Python/SQL notebooks that run inside Snowflake. Support Snowpark, ML libraries, and can be created programmatically via Cortex Code.", "icon": "description"},
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


st.divider()
st.markdown("#### Snowpark ML Continued — Feature Store, Model Registry & Notebooks")
st.caption("Now we'll build the same congestion prediction problem as a full ML pipeline inside a Snowflake Notebook, using Feature Store for feature management and Model Registry for versioning.")

st.warning("**Before continuing:** Open **Workspaces** in Snowflake (Snowsight) before running the next prompt. Cortex Code needs Workspaces enabled to create and manage Snowflake Notebooks.", icon=":material/warning:")

PROMPT_4_4 = """In PORT_AI_DEMO.PORT_OPS, create a Snowflake Notebook called CONGESTION_ML_NOTEBOOK that builds an end-to-end ML pipeline using Snowflake's Feature Store and Model Registry. The notebook should have these sections:

SECTION 1 - Setup & Feature Store:
- Import snowflake.ml.feature_store (FeatureStore, FeatureView, Entity, CreationMode)
- Create a Feature Store in the PORT_OPS schema using the PORT_AI_WH warehouse
- Register a MANIFEST entity with MANIFEST_ID as the join key
- Create a managed Feature View called CONGESTION_FEATURE_VIEW that:
  - Queries CONTAINER_MANIFESTS joined with TERMINALS
  - Includes the same features as our CONGESTION_FEATURES view (teu_count, weight_tonnes, terminal_type, num_berths, cargo_category, arrival_month, arrival_day_of_week, is_peak_season, cbsa_declaration_status)
  - Includes IS_CONGESTED as the label
  - Uses a 1-hour refresh frequency so features stay current
  - Has a timestamp_col for point-in-time correctness

SECTION 2 - Training Dataset Generation:
- Use fs.generate_dataset() with a spine DataFrame to create a point-in-time correct training dataset
- Split into train (80%) and test (20%) sets

SECTION 3 - Train Multiple Models:
- Train three traditional ML models on the same training data:
  1. XGBoost classifier (xgboost.XGBClassifier)
  2. Random Forest (sklearn.ensemble.RandomForestClassifier)
  3. Logistic Regression (sklearn.linear_model.LogisticRegression)
- For each model, calculate accuracy, precision, recall, and F1 score on the test set
- Display a comparison table of all three models side by side

SECTION 4 - Register Best Model:
- Identify which model performed best by F1 score
- Use snowflake.ml.registry.Registry to register the best model with log_model()
- Name it CONGESTION_PREDICTOR, version V1
- Include sample_input_data for schema inference and explainability
- Set target_platforms to WAREHOUSE so it can be called via SQL
- Log the evaluation metrics on the model version

SECTION 5 - Validate Registered Model:
- Run SHOW MODELS in the schema to confirm registration
- Test the registered model by calling MODEL(PORT_AI_DEMO.PORT_OPS.CONGESTION_PREDICTOR, V1)!PREDICT() on sample data from the test set
- Compare the registered model's predictions with the in-memory predictions to confirm they match

Make the notebook well-documented with markdown cells explaining each section.

Do NOT run the notebook — just create it. We will run it in the next step."""

render_prompt("Prompt 4.4", "Create ML Pipeline Notebook", PROMPT_4_4)

render_explanation("What this prompt does", """
Creates a **Snowflake Notebook** with a complete ML pipeline that uses three key Snowflake ML services:

**Feature Store** (`snowflake.ml.feature_store`):
```python
fs = FeatureStore(
    session=session,
    database="PORT_AI_DEMO",
    name="PORT_OPS",
    default_warehouse="PORT_AI_WH",
    creation_mode=CreationMode.CREATE_IF_NOT_EXIST
)

entity = Entity(name="MANIFEST", join_keys=["MANIFEST_ID"])
fs.register_entity(entity)

fv = FeatureView(
    name="CONGESTION_FEATURE_VIEW",
    entities=[entity],
    feature_df=feature_query_df,
    timestamp_col="ARRIVAL_DATE",
    refresh_freq="1 hour"
)
fv = fs.register_feature_view(fv, version="V1")
```
Feature views are backed by **Dynamic Tables** — Snowflake automatically keeps them refreshed.

**Training dataset with point-in-time correctness**:
```python
dataset = fs.generate_dataset(
    name="CONGESTION_TRAINING_DATA",
    spine_df=spine_df,
    features=[fv],
    spine_timestamp_col="ARRIVAL_DATE",
    spine_label_cols=["IS_CONGESTED"]
)
```
This prevents **data leakage** — each row only sees features available at the time of that record.

**Model comparison** trains three classifiers and picks the best:
- **XGBoost**: Gradient boosted trees — typically best for tabular data
- **Random Forest**: Ensemble of decision trees — robust, less prone to overfitting
- **Logistic Regression**: Linear model — fast, interpretable baseline

**Model Registry** (`snowflake.ml.registry.Registry`):
```python
reg = Registry(session=session, database_name="PORT_AI_DEMO", schema_name="PORT_OPS")
mv = reg.log_model(
    best_model,
    model_name="CONGESTION_PREDICTOR",
    version_name="V1",
    sample_input_data=X_test.head(5),
    target_platforms=["WAREHOUSE"],
    metrics={"f1": best_f1, "accuracy": best_acc}
)
```
Once registered, the model becomes a SQL-callable Snowflake object.

**Why this matters**: Prompts 4.1-4.3 used Snowflake's built-in AutoML (zero code). This notebook shows the alternative — training your own models with full control over algorithm choice, hyperparameters, and evaluation. Both approaches register models as first-class Snowflake objects.
""")


PROMPT_4_5 = """Open the CONGESTION_ML_NOTEBOOK in Snowsight and run all cells. After execution completes, show me:

1. The feature store entities and feature views: list them with SQL (SHOW FEATURE VIEWS IN SCHEMA PORT_AI_DEMO.PORT_OPS)
2. The model comparison results — which model won and by how much?
3. The registered model: SHOW MODELS IN SCHEMA PORT_AI_DEMO.PORT_OPS and SHOW FUNCTIONS IN MODEL PORT_AI_DEMO.PORT_OPS.CONGESTION_PREDICTOR
4. A SQL query that uses the registered model for inference:
   SELECT MANIFEST_ID,
          MODEL(PORT_AI_DEMO.PORT_OPS.CONGESTION_PREDICTOR, V1)!PREDICT(teu_count, weight_tonnes, terminal_type, num_berths, cargo_category, arrival_month, arrival_day_of_week, is_peak_season, cbsa_declaration_status) AS prediction
   FROM CONGESTION_FEATURES
   LIMIT 10;"""

render_prompt("Prompt 4.5", "Run Notebook & Verify", PROMPT_4_5)

render_explanation("What this prompt does", """
Runs the notebook end-to-end and verifies all artifacts were created:

**Feature Store verification**:
- `SHOW FEATURE VIEWS` lists managed feature views with their backing Dynamic Table, refresh frequency, and status
- Feature views marked as `ACTIVE` are being refreshed automatically by Snowflake

**Model comparison**: The notebook prints a side-by-side table like:
| Model | Accuracy | Precision | Recall | F1 |
|-------|----------|-----------|--------|----|
| XGBoost | 0.85 | 0.82 | 0.79 | 0.80 |
| Random Forest | 0.83 | 0.80 | 0.76 | 0.78 |
| Logistic Regression | 0.78 | 0.74 | 0.71 | 0.72 |

**Model Registry verification**:
- `SHOW MODELS` confirms the model object exists
- `SHOW FUNCTIONS IN MODEL` lists callable methods (PREDICT, PREDICT_PROBA)

**SQL inference**: The `MODEL(name, version)!PREDICT()` syntax calls the registered model directly from SQL — no Python needed. This is what makes Snowflake ML unique: models trained in Python become SQL functions accessible to any analyst.
""")


render_key_concepts([
    {"term": "Snowflake ML Classification", "definition": "Snowflake's built-in AutoML for binary and multi-class classification. It automatically handles feature encoding, model selection, hyperparameter tuning, and evaluation. Models are stored as first-class Snowflake objects."},
    {"term": "Feature Engineering", "definition": "The process of transforming raw data into features that better represent the underlying problem for ML models. Good features are often more important than complex algorithms."},
    {"term": "SYSTEM$REFERENCE", "definition": "A Snowflake system function that creates a secure, permissions-aware reference to a database object. Required when passing tables or views to ML training functions."},
    {"term": "Confusion Matrix", "definition": "A 2x2 table showing True Positives, False Positives, True Negatives, and False Negatives. The foundation for calculating precision, recall, F1 score, and other classification metrics."},
    {"term": "Feature Store", "definition": "A centralized repository for ML features (snowflake.ml.feature_store). You register Entities (join keys like MANIFEST_ID), then create Feature Views — managed (backed by Dynamic Tables with automatic refresh) or external (backed by views). The store provides generate_dataset() for point-in-time correct training data and retrieve_feature_values() for inference."},
    {"term": "Model Registry", "definition": "Snowflake's native model versioning system (snowflake.ml.registry.Registry). Use log_model() to register any Python model (sklearn, XGBoost, etc.) as a first-class Snowflake object. Registered models can be called via SQL with MODEL(name, version)!PREDICT() and support explainability via SHAP."},
    {"term": "Snowflake Notebook", "definition": "An interactive notebook that runs inside Snowflake with access to Snowpark, snowflake-ml-python, and other libraries. Notebooks can mix SQL and Python cells, and are created as Snowflake objects that can be shared via RBAC."},
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
    "Snowflake Notebook with end-to-end ML pipeline",
    "Feature Store with MANIFEST entity and CONGESTION_FEATURE_VIEW",
    "XGBoost, Random Forest, and Logistic Regression models compared",
    "Best model registered in Snowflake Model Registry with explainability",
])
