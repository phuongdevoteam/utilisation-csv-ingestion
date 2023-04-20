{% set project = ti.xcom_pull(task_ids = params.task_id)['target_project_id'] %}
{% set dataset = ti.xcom_pull(task_ids = params.task_id)['target_dataset'] %}

CREATE TABLE IF NOT EXISTS `{{ project }}.{{ dataset }}.example_Source`
(
    StockId INT64,
    ChangedDate TIMESTAMP,
    StockLevel INT64,
    StorageLocation STRING,
    batch_number STRING OPTIONS(description=""),
    DWH_TIMESTAMP TIMESTAMP OPTIONS(description=""),
    extraction_timestamp TIMESTAMP OPTIONS(description="")
);