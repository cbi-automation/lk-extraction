def process_all_markers(text, kuartal):
    all_output = {}
    company = Company()

    for marker_name, marker_pairs in marker_config.items():
        function_name = marker_to_function.get(marker_name)
        if not function_name:
            continue

        func = globals().get(function_name)
        if not func:
            print(f"[⚠️] Fungsi '{function_name}' tidak ditemukan.")
            continue

        output = func(marker_pairs, text, kuartal)
        all_output.update(output)

    return all_output