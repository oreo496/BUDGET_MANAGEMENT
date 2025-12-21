from typing import Optional, Dict, Any

# Lazy imports to avoid heavy deps unless used

def _import_tf():
    try:
        import tensorflow as tf
        return tf
    except Exception as e:
        raise RuntimeError("TensorFlow is required for Keras training utilities. Install tensorflow.")


def _import_matplotlib():
    import matplotlib.pyplot as plt
    return plt


class AccuracyGapStop:
    """Keras callback: early terminate if training vs validation accuracy gap exceeds margin."""
    def __init__(self, margin: float = 0.05, min_epoch: int = 1):
        self.margin = margin
        self.min_epoch = min_epoch
        self.model = None
        self.history = []

    def set_model(self, model):
        self.model = model

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        train_acc = logs.get('accuracy') or logs.get('acc')
        val_acc = logs.get('val_accuracy') or logs.get('val_acc')
        if train_acc is None or val_acc is None:
            return
        gap = float(train_acc) - float(val_acc)
        self.history.append({'epoch': epoch, 'train_acc': float(train_acc), 'val_acc': float(val_acc), 'gap': gap})
        if epoch + 1 >= self.min_epoch and gap > self.margin:
            # Stop training due to overfitting signal
            self.model.stop_training = True


def train_keras_with_early_stopping(
    model,
    x_train,
    y_train,
    batch_size: int = 32,
    epochs: int = 50,
    validation_split: float = 0.2,
    patience: int = 8,
    acc_gap_margin: float = 0.05,
    metrics: Optional[list] = None,
    audit_logger=None,
    plot_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Train a Keras model with EarlyStopping (monitor val_loss), soft-cap accuracy gap stop,
    and restore_best_weights=True, plus plot train/val loss.
    Returns dict with model, history, stopped_reason, and plot path (if generated).
    """
    tf = _import_tf()
    metrics = metrics or ['accuracy']
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=metrics)

    early = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', mode='min', patience=patience, restore_best_weights=True, verbose=1
    )
    acc_gap_cb = AccuracyGapStop(margin=acc_gap_margin, min_epoch=max(1, patience // 2))

    # Keras requires callbacks to be instances of tf.keras.callbacks.Callback
    class _AccGapWrapper(tf.keras.callbacks.Callback):
        def __init__(self, cb: AccuracyGapStop):
            super().__init__()
            self._cb = cb
        def on_epoch_end(self, epoch, logs=None):
            self._cb.set_model(self.model)
            self._cb.on_epoch_end(epoch, logs)

    history = model.fit(
        x_train, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=validation_split,
        callbacks=[early, _AccGapWrapper(acc_gap_cb)],
        verbose=1,
    )

    logs = history.history
    train_loss = logs.get('loss', [])
    val_loss = logs.get('val_loss', [])

    # Visual confirmation: Training vs Validation Loss plot
    plot_file = None
    try:
        plt = _import_matplotlib()
        plt.figure(figsize=(7,4))
        plt.plot(train_loss, label='Training Loss')
        plt.plot(val_loss, label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.tight_layout()
        plot_file = plot_path or 'training_loss_plot.png'
        plt.savefig(plot_file)
        plt.close()
    except Exception:
        pass

    # Overfitting warning if divergence
    warning = None
    if len(train_loss) > 5 and len(val_loss) > 5:
        # Simple divergence heuristic: last val_loss - last train_loss > 10% of val_loss
        try:
            if (val_loss[-1] - train_loss[-1]) / max(val_loss[-1], 1e-8) > 0.10:
                warning = 'Warning: Potential Overfitting Detected'
                if audit_logger is not None:
                    try:
                        audit_logger.log(
                            user_id=-1,
                            decision_type='model_training_warning',
                            severity='MEDIUM',
                            trigger_reason=warning,
                            model_confidence_score=None,
                            model_used='keras_early_stopping'
                        )
                    except Exception:
                        pass
        except Exception:
            pass

    stopped_reason = None
    if len(acc_gap_cb.history) > 0 and acc_gap_cb.history[-1]['gap'] > acc_gap_margin:
        stopped_reason = 'accuracy_gap_exceeded'
    elif 'val_loss' in logs and len(logs['val_loss']) < epochs:
        stopped_reason = 'early_stopping_patience'

    return {
        'model': model,
        'history': history,
        'stopped_reason': stopped_reason,
        'plot_file': plot_file,
        'overfitting_warning': warning,
    }


# Minimal PyTorch/TabNet-style manual loop stub (non-executed unless called)

def train_tabnet_with_early_stopping(
    model,
    train_loader,
    val_loader,
    optimizer,
    loss_fn,
    epochs: int = 50,
    patience: int = 8,
    acc_gap_margin: float = 0.05,
    audit_logger=None,
) -> Dict[str, Any]:
    """
    Generic manual training loop with early stopping and best-weight restore for TabNet/PyTorch.
    Note: Expects model to implement .train()/.eval() and standard forward/pass.
    """
    import copy
    best_state = None
    best_val_loss = float('inf')
    wait = 0
    logs = {'loss': [], 'val_loss': [], 'acc': [], 'val_acc': []}

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        for xb, yb in train_loader:
            optimizer.zero_grad()
            out = model(xb)
            loss = loss_fn(out, yb)
            loss.backward()
            optimizer.step()
            train_loss += float(loss.item())
            # accuracy calc assumes classification
            preds = out.argmax(dim=1)
            train_correct += int((preds == yb).sum().item())
            train_total += int(yb.size(0))

        train_loss /= max(1, len(train_loader))
        train_acc = train_correct / max(1, train_total)

        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with __import__('torch').no_grad():
            for xb, yb in val_loader:
                out = model(xb)
                vloss = loss_fn(out, yb)
                val_loss += float(vloss.item())
                preds = out.argmax(dim=1)
                val_correct += int((preds == yb).sum().item())
                val_total += int(yb.size(0))
        val_loss /= max(1, len(val_loader))
        val_acc = val_correct / max(1, val_total)

        logs['loss'].append(train_loss)
        logs['val_loss'].append(val_loss)
        logs['acc'].append(train_acc)
        logs['val_acc'].append(val_acc)

        # Early stopping on val_loss
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = copy.deepcopy(model.state_dict())
            wait = 0
        else:
            wait += 1
            if wait >= patience:
                break

        # Soft-cap: accuracy gap
        if (train_acc - val_acc) > acc_gap_margin and epoch >= max(1, patience // 2):
            break

    # Restore best weights
    if best_state is not None:
        model.load_state_dict(best_state)

    warning = None
    if len(logs['val_loss']) >= 5 and (logs['val_loss'][-1] - logs['loss'][-1]) / max(logs['val_loss'][-1], 1e-8) > 0.10:
        warning = 'Warning: Potential Overfitting Detected'
        if audit_logger is not None:
            try:
                audit_logger.log(
                    user_id=-1,
                    decision_type='model_training_warning',
                    severity='MEDIUM',
                    trigger_reason=warning,
                    model_used='tabnet_early_stopping'
                )
            except Exception:
                pass

    return {'model': model, 'logs': logs, 'overfitting_warning': warning}
