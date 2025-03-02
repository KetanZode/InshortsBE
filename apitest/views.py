from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from django.apps import apps
from django.views import View
import json

class GetModels(APIView):
    def post(self, request):
        data        = request.data
        p_apps      = data.get('apps',[])
        app_list    = [x for x in apps.all_models]
        print(app_list)
        all_res     = {}

        for app in p_apps:
            if app in app_list:
                models = apps.get_app_config(app).get_models()
                response = {}
                for model in models :                   
                    app_name    = app
                    model_name  = model.__name__
                    try:
                        # Retrieve the model
                        model = apps.get_model(app_name, str(model_name))
                        if not model:
                            return Response({"error": f"Model '{model_name}' not found in app '{app_name}'"}, status=404)

                        # Get all field names
                        m_data  = model._meta.get_fields()
                        fields  = [{"name": field.name, "type": field.get_internal_type()} for field in model._meta.get_fields()]
                        response[model_name] = fields 
                    except LookupError:
                        return Response({"error": f"App '{app_name}' or model '{model_name}' not found"}, status=404)
                all_res[app] = response
        return Response(all_res)

class GetModels2(APIView):
    def post(self, request):
        data = request.data
        requested_apps = data.get('apps', [])  # List of requested app names

        # Get a list of all installed Django apps
        available_apps = {app_config.label for app_config in apps.get_app_configs()}

        all_res = {}
        errors = {}

        for app in requested_apps:
            if app not in available_apps:
                errors[app] = f"App '{app}' not found."
                continue  # Skip to the next app instead of stopping execution

            models = apps.get_app_config(app).get_models()
            response = {}

            for model in models:
                model_name = model.__name__
                try:
                    # Retrieve the model dynamically
                    model = apps.get_model(app, model_name)

                    # Extract detailed field information
                    fields = []
                    for field in model._meta.get_fields():
                        field_info = {
                            "name": field.name,
                            "type": field.get_internal_type(),
                            "primary_key": getattr(field, "primary_key", False),
                            "nullable": field.null,
                            "unique": getattr(field, "unique", False),
                            # "default": field.default if getattr(field, "unique", None) is not None else None,
                        }

                        # Check for ForeignKey, ManyToMany, OneToOne relationships
                        if isinstance(field, ForeignKey):
                            field_info["relation"] = {
                                "type": "ForeignKey",
                                "related_model": f"{field.related_model._meta.app_label}.{field.related_model.__name__}"
                            }
                        elif isinstance(field, ManyToManyField):
                            field_info["relation"] = {
                                "type": "ManyToManyField",
                                "related_model": f"{field.related_model._meta.app_label}.{field.related_model.__name__}"
                            }
                        elif isinstance(field, OneToOneField):
                            field_info["relation"] = {
                                "type": "OneToOneField",
                                "related_model": f"{field.related_model._meta.app_label}.{field.related_model.__name__}"
                            }

                        fields.append(field_info)

                    response[model_name] = fields
                except LookupError:
                    errors[f"{app}.{model_name}"] = f"Model '{model_name}' not found in app '{app}'."
            
            all_res[app] = response

        # Final response structure
        response_data = {"models": all_res}
        # if errors:
        #     response_data["errors"] = errors  # Include errors if any app/model lookup failed

        return Response(json.loads(json.dumps(response_data)))



class GetMermaidERDiagram( View):
    def post(self, request):
        data = request.data
        requested_apps = data.get('apps', [])  # List of requested app names

        # Get all installed Django apps
        available_apps = {app_config.label for app_config in apps.get_app_configs()}

        entities = []  # Stores table definitions
        relationships = []  # Stores relationships
        errors = {}

        for app in requested_apps:
            if app not in available_apps:
                errors[app] = f"App '{app}' not found."
                continue  # Skip to the next app instead of stopping execution

            models = apps.get_app_config(app).get_models()

            for model in models:
                model_name = model.__name__
                try:
                    # Retrieve the model dynamically
                    model = apps.get_model(app, model_name)

                    # Table definition
                    table_def = f"    {model_name} {{"

                    for field in model._meta.get_fields():
                        field_type = field.get_internal_type()
                        field_constraints = []

                        if getattr('field','PK',False):
                            field_constraints.append("PK")
                        if getattr(field, "unique", False):
                            field_constraints.append("UNIQUE")
                        if field.null:
                            field_constraints.append("NULL")

                        constraints = " ".join(field_constraints).strip()
                        table_def += f"\n        {field.name} {field_type} {constraints}"

                        # Handle relationships
                        if isinstance(field, ForeignKey):
                            relationships.append(f"    {model_name} ||--|{{ {field.related_model.__name__} : \"{field.name}\" }}")
                        elif isinstance(field, ManyToManyField):
                            relationships.append(f"    {model_name} }}|--|{{ {field.related_model.__name__} : \"{field.name}\"  }}")
                        elif isinstance(field, OneToOneField):
                            relationships.append(f"    {model_name} ||--|| {field.related_model.__name__} : \"{field.name}\"")

                    table_def += "\n    }"
                    entities.append(table_def)
                except LookupError:
                    errors[f"{app}.{model_name}"] = f"Model '{model_name}' not found in app '{app}'."

        # Generate Mermaid.js ER diagram syntax
        mermaid_er = "erDiagram\n" + "\n".join(entities) + "\n" + "\n".join(relationships)
        print('reached')
        return render(request, 'diagram.html', {"mermaid_er": mermaid_er})
        response_data = {"mermaid_er": mermaid_er}
        if errors:
            response_data["errors"] = errors  # Include errors if any app/model lookup failed

        return Response(response_data)


class RenderDiagram(View):
    def get(self, request):
        # Hardcoded Mermaid.js ER Diagram String (Properly formatted)
        mermaid_er = """erDiagram
        Source {
            id AutoField PK
            name CharField UNIQUE
            created_at DateTimeField
            category ForeignKey
            tags 
        }
        """
        data = {
                    "apps":["infonow","admin","auth"]
                }
        requested_apps = data.get('apps', [])  # List of requested app names

        # Get all installed Django apps
        available_apps = {app_config.label for app_config in apps.get_app_configs()}

        entities = []  # Stores table definitions
        relationships = []  # Stores relationships
        errors = {}

        for app in requested_apps:
            if app not in available_apps:
                errors[app] = f"App '{app}' not found."
                continue  # Skip to the next app instead of stopping execution

            models = apps.get_app_config(app).get_models()

            for model in models:
                model_name = model.__name__
                try:
                    # Retrieve the model dynamically
                    model = apps.get_model(app, model_name)

                    # Table definition
                    table_def = f"    {model_name} {{"

                    for field in model._meta.get_fields():
                        field_type = field.get_internal_type()
                        field_constraints = []

                        if getattr('field','PK',False):
                            field_constraints.append("PK")
                        if getattr(field, "unique", False):
                            field_constraints.append("UK")
                        # if field.null:
                        #     field_constraints.append("NULL")

                        constraints = " ".join(field_constraints).strip()
                        table_def += f"\n        {field.name} {field_type} {constraints}"

                        # # Handle relationships
                        # if isinstance(field, ForeignKey):
                        #     relationships.append(f"    {model_name} ||--|{{ {field.related_model.__name__} : \"{field.name}\" }}")
                        # elif isinstance(field, ManyToManyField):
                        #     relationships.append(f"    {model_name} }}|--|{{ {field.related_model.__name__} : \"{field.name}\"  }}")
                        # elif isinstance(field, OneToOneField):
                        #     relationships.append(f"    {model_name} ||--|| {field.related_model.__name__} : \"{field.name}\"")

                    table_def += "\n    }"
                    entities.append(table_def)
                except LookupError:
                    errors[f"{app}.{model_name}"] = f"Model '{model_name}' not found in app '{app}'."

        # Generate Mermaid.js ER diagram syntax
        mermaid_er = "erDiagram\n" + "\n".join(entities) + "\n" + "\n".join(relationships)
        print(mermaid_er)
        print('reached')
        return render(request, 'diagram.html', {"mermaid_er": mermaid_er})
